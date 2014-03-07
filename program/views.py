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
from .library import SolutionValidator

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
		fields = ['teamName', 'compiler']

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
			return render(request, 'program/accounts/login_styled.html', 
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

		''' retrieve the problem results, then build a dictionary. key = problem id '''
		'''problemResultsArray= ProblemResult.objects.filter(user=request.user)
		problemResultsDict = {}
		for result in problemResultsArray:
			problemResultsDict[result.problem.id] = result
		problemResults = []
		for p in problems:
			problemResults.append(problemResultsDict.get(p.id, None))

		'''
		userdata = UserSettings.objects.get(user=request.user)
		problemResultsAll = ProblemResult.objects.filter(user=request.user)

		# compile all successful problem results for each problem
		problemResults = []
		for p in problems:
			prp = problemResultsAll.filter(problem=p)
			result = None
			try:
				result = prp[0]
			except IndexError:
				pass
			problemResults.append(result)

		# compile possible scores
		possibleScores = []
		for p in problems:
			possibleScores.append(ProblemScore.possibleScore(userdata, p))

		data = zip(problems, possibleScores, problemResults)
		return render(request, 'program/team/problem_list.html', {
			'data': data
			})
# ============

class ProblemDetailView(View):
	def get(self, request, problemId):
		problem = Problem.objects.get(pk=problemId)
		submissions = ProblemResult.objects.filter(user=request.user, problem=problem)
		userdata = UserSettings.objects.get(user=request.user)
		return render(request, "program/team/problem_detail.html", 
			{
				'problem' 		: problem,
				'testForm'		: TestForm(),
				'submissions'	: submissions,
				'possibleScore' : ProblemScore.possibleScore(userdata, problem),
				'latestSubmission' : submissions[0] if len(submissions) > 0 else False,
			})

	def post(self, request, problemId):
		# Handle file upload
		form = TestForm(request.POST, request.FILES)
		if form.is_valid:
			solution = ProblemSolution(solution=request.FILES['solution'], owner=request.user)
			solution.save()
			return redirect("/program/problem/%s/submit/%s" % (problemId, solution.id))
		return HttpResponseRedirect("index")
		"""
		form = TestForm(request.POST)
		if form.is_valid():
			solution = ProblemSolution(request.POST, request.FILES)
			solution.owner = request.user
			solution.save()
			return HttpResponseRedirect("problems")
		"""
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
		except (Problem.DoesNotExist, ProblemResult.DoesNotExist):
			pass
# ============	

class ProblemExecutionView(View):
	def get(self, request, problemId, fileId):
		"""
		class ThreadedCommand:
			def __init__(self, cmd):
				self.command = cmd
				self.process = None

				self.stdout = None
				self.stderr = None
				self.exitCode = None
			def run(self, timeout):
				def target():
					print 'Thread started'
					self.process = subprocess.Popen(self.cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
					self.stdout = self.process.communicate()[0]
					self.exitCode = self.process.returncode
					print 'Thread finished'

				thread = threading.Thread(target=target)
				thread.start()

				thread.join(timeout)
				if thread.is_alive():
					print 'Terminating process'
					self.process.terminate()
					thread.join()
		"""

		solution = ProblemSolution.objects.get(pk=fileId)
		problem = Problem.objects.get(pk=problemId)
		
		from .tasks import testSolution
		testSolution.delay(problem, request.user, solution)

		return redirect('problems')
# ============

class WaitView(View):
	def get(self, request):
		submission = ProblemResult.objects.filter(user=request.user, successful=True).first()
		subDate = None
		subTime = None
		if submission:
			subDate = submission.submissionTime.date()
			subTime = submission.submissionTime.astimezone(timezone(settings.TIME_ZONE)).timetz().strftime("%I:%M:%S %p")
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
			fdsafds # TODO
			return redirect('user settings')
# ============

class ScoreboardView(View):
	def get(self, request):
		pass
		users = UserSettings.objects.all().order_by('-score')
		problems = Problem.objects.all()
		results = ProblemResult.objects.all()

		tableData = []
		rank = 1
		for u in users:
			resultsList = []
			userQuerySet = results.filter(user=u.user)
			for p in problems:
				resultsList.append( userQuerySet.filter(problem=p).first() )
			tableData.append( (rank, u, resultsList) )
			rank += 1

		return render(request, "program/scoreboards/scoreboard.html", {
			"tableData" : tableData,
			"problems"	: problems,
			})
# ============



