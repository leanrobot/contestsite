from __future__ import absolute_import

import subprocess, threading
from datetime import datetime

from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import HttpResponse
from django import forms
import django.contrib.auth as auth
from django.conf import settings


from pytz import timezone

from .models import *
from .library import SolutionValidator, fixedTZData, progressBar
from .tasks import testSolution

# Helper Functions =============================================

def checkCorrectSolution(problem, stdin, stdout, stderr, exitCode):
	stdoutMatch = problem.outputSubmit == stdout
	exitCodeCorrect = exitCode == 0
	fdsafsd
	return stdoutMatch and exitCodeCorrect



# Forms ========================================================

class LoginForm(forms.Form):
	username 	= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter username'}))
	password 	= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter password'}))
	next		= forms.CharField(widget=forms.HiddenInput)

class TestForm(forms.Form):
	solution = forms.FileField(label="Select a solution")

class UserSettingsForm(forms.ModelForm):
	class Meta:
		model = UserSettings
		fields = ['teamName']

# Views ==========================================================

class IndexView(View):
	def get(self, request):
		return render(request, "program/index.html", {})
# ============

class LoginPage(View):
	def get(self, request):
		loginForm = LoginForm()
		redirect_url = "index"
		if 'next' in request.GET:
			redirect_url = request.GET['next']
		loginForm.fields['next'].initial = redirect_url

		if request.user.is_authenticated():
			return redirect(redirect_url)
		else:
			return render(request, 'program/accounts/login.html', 
				{'form':LoginForm()})

	def post(self, request):
		response = redirect("index")

		if not request.user.is_authenticated():
			usernm = request.POST['username']
			passwd = request.POST['password']
			user = auth.authenticate(username=usernm, password=passwd)

			response = redirect('login')
			if user is not None and user.is_active:
				auth.login(request, user)
				if request.POST['next']:
					response = redirect(request.POST['next'])

		return response
# ============

class LogoutPage(View):
	def get(self, request):
		auth.logout(request)

		redirectUrl = 'index'
		if 'next' in request.GET:
			redirectUrl = request.GET['next']

		return redirect(redirectUrl)
# ============

class ProblemListView(View):
	def get(self, request):
		problems = Problem.objects.all()

		user = request.user
		userdata = UserSettings.objects.get(user=user)
		problemResultsAll = ProblemResult.objects.filter(user=request.user)

		scores = []
		results = []
		correct = []
		failed = []
		pending = []

		for p in problems:
			# compute the possible score
			scores.append(p.possibleScore(user))
			# retrieve the latest submission, none if no submission
			latest = p.latestSubmission(user)
			# add the result to the data for table
			results.append(latest)

			# populate table helper variables
			if latest:
				correct.append( latest.successful and latest.graded )
				failed.append( p.failed(user) )
				pending.append( not latest.graded )
			else:
				correct.append(False)
				failed.append(False)
				pending.append(False)

		data = zip(problems, scores, results, correct, failed, pending)
		return render(request, 'program/team/problem_list.html', {
			'data': data
			})
# ============

class ProblemDetailView(View):
	def get(self, request, problemId):
		# handle error
		error = None
		if 'error' in request.GET:
			errorCode = request.GET['error']
			if errorCode == "nofile":
				error = "Please select a file."
			elif errorCode == "nocompiler":
				error = "Unsupported Compiler."

		problem = Problem.objects.get(pk=problemId)
		submissions = ProblemResult.objects.filter(user=request.user, problem=problem)
		userdata = UserSettings.objects.get(user=request.user)

		latestSubmission = submissions[0] if len(submissions) > 0 else False

		pending = False if latestSubmission == False else not latestSubmission.graded
		failed = problem.failed(request.user)
		correct = False if latestSubmission == False else latestSubmission.successful
		return render(request, "program/team/problem_detail.html", 
			{
				'problem' 		: problem,
				'testForm'		: TestForm(),
				'submissions'	: submissions,
				'possibleScore' : problem.possibleScore(userdata.user),
				'latestSubmission' : latestSubmission,
				'correct'		: correct,
				'pending'		: pending,
				'failed'		: failed,
				'error'			: error,
			})

	def post(self, request, problemId):
		# Handle file upload
		form = TestForm(request.POST, request.FILES)
		try:
			if form.is_valid:
				solution = ProblemSolution(solution=request.FILES['solution'], owner=request.user)
				solution.save()
				return redirect("/team/problem/%s/submit/%s" % (problemId, solution.id))
		except:
			response = redirect('problem detail', problemId)
			response['Location'] = "?error=nofile"
			return response

		# should never happen
		return HttpResponseRedirect("index")
# ============

class ProblemResultView(View):
	def get(self, request, problemId, resultId):
		pass
		try:
			problem = Problem.objects.get(pk=problemId)
			result 	= ProblemResult.objects.get(pk=resultId)
			execution = result.executionresult
			minutesAgo = (datetime.now(tz=timezone(settings.TIME_ZONE)) - result.submissionTime).total_seconds() // 60
			runningTime = (execution.endTime - execution.startTime).total_seconds()

			return render(request, "program/team/result.html", {
					"problem"	: problem,
					"result"	: result,
					"execution"	: result.executionresult,

					"runningTime": runningTime,
					"test"		: True,

				})
		except (Problem.DoesNotExist, ProblemResult.DoesNotExist, ExecutionResult.DoesNotExist):
			pass # TODO add exception handling
# ============	

class ProblemExecutionView(View):
	def get(self, request, problemId, fileId):
		solution = ProblemSolution.objects.get(pk=fileId)
		problem = Problem.objects.get(pk=problemId)
		solution.save()
		problem.save()

		tz = timezone(settings.TIME_ZONE)
		now = datetime.now(tz=tz)
		result = ProblemResult(
				submissionTime=now,
				successful=False,
				user=request.user,
				problem=problem,
		)
		result.save()
		execution = ExecutionResult(
			startTime = now,
			endTime = now,
			stdin = "",
			stdout = "",
			stderr = "",
			diff = "",
			filename = "",
			command = "",
			exitCode = -999,
			problemResult = result
		)
		execution.save()
		
		# Send the problem to the queue.
		testSolution.delay(problem, request.user, result, execution, solution)

		return redirect('problem detail', problemId)
		#return redirect('problems')
# ============

class TextFileGeneratorView(View):
	def get(self, request, problemId):
		problem = Problem.objects.get(pk=problemId)
		response = render(request, "program/team/textFile.html", {
			"data" : problem.inputTest,
			},
			content_type="text/plain")
		if problem.inputType == 'file':
			response['Content-Disposition'] = 'attachment; filename=%s' % problem.filename
		return response
# ============


class WaitView(View):
	def get(self, request):
		submission = None
		subDate = None
		subTime = None

		if(not request.user.is_anonymous()):
			submission = ProblemResult.objects.filter(user=request.user, successful=True).first()
		if submission:
			subDate = submission.submissionTime.date()
			subTime = fixedTZData(submission.submissionTime)#submission.submissionTime.astimezone(timezone(settings.TIME_ZONE)).timetz().strftime("%I:%M:%S %p")
		return render(request, "program/contestNotInSession.html", {
			'now'				: datetime.now(tz=timezone(settings.TIME_ZONE)),
			'submission'		: submission,
			'subDate'			: subDate,
			'subTime'			: subTime,
			})
# ============

class UserSettingsView(View):
	def get(self, request):
		form = UserSettingsForm()
		settings = None

		try:
			settings = UserSettings.objects.get(user=request.user)
		except UserSettings.DoesNotExist:
			settings = None
		if settings:
			form = UserSettingsForm(instance=settings)
		return render(request, "program/accounts/settings.html", {
			'userSettingsForm' : form,
			})

	def post(self, request):
		pass
		# TODO write this
		userSettings = UserSettings(user=request.user)
		form = UserSettingsForm(request.POST, instance=userSettings)
		if form.is_valid():
			form.save()
			return redirect('index')
		else:
			return redirect('user settings')
# ============

class ScoreboardView(View):
	def get(self, request):
		pass
		users = UserSettings.objects.all()
		users = filter(lambda us: not( us.user.is_staff or us.user.is_superuser), users)
		# sort the users by score from high -> low.
		users = reversed(sorted(users, key=lambda user: user.score() ))

		tableData = []
		rank = 1

		for u in users:
			resultsList = []

			(correct, failed) = progressBar(u.user)

			tableData.append( (rank, u, resultsList, correct, failed) )
			rank += 1

		return render(request, "program/scoreboards/scoreboard.html", {
			"tableData" : tableData,
			#"problems"	: problems,
			})
# ============

class TestView(View):
	def get(self, request):
		return render(request, "program/test.html", {

			})



