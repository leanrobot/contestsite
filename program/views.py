import subprocess, threading, datetime

from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import HttpResponse
from django import forms
import django.contrib.auth as auth
from django.conf import settings

from pytz import timezone

from program.models import *
from program.library import SolutionValidator

# Helper Functions =============================================

def checkCorrectSolution(problem, stdin, stdout, stderr, exitCode):
	stdoutMatch = problem.outputSubmit == stdout
	exitCodeCorrect = exitCode == 0
	fdsafsd
	return stdoutMatch and exitCodeCorrect

# Forms ========================================================

class LoginForm(forms.Form):
	username 	= forms.CharField()
	password 	= forms.CharField(widget=forms.PasswordInput)
	next		= forms.CharField(widget=forms.HiddenInput)

class TestForm(forms.Form):
	solution = forms.FileField(label="Select a solution")

# Create your views here.
class IndexView(View):
	def get(self, request):
		return render(request, "program/index.html", {})



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
		response = redirect('/')

		if not request.user.is_authenticated():
			usernm = request.POST['username']
			passwd = request.POST['password']
			user = auth.authenticate(username=usernm, password=passwd)

			response = redirect('login')
			if user is not None and user.is_active:
				auth.login(request, user)
				response = HttpResponse(request.POST['next'])

		return response

class LogoutPage(View):
	def get(self, request):
		auth.logout(request)

		redirectUrl = 'index'
		if 'next' in request.GET:
			redirectUrl = request.GET['next']

		return redirect(redirectUrl)

class TeamProblemPage(View):
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
		problemResultsAll = ProblemResult.objects.filter(user=request.user)

		problemResults = []
		for p in problems:
			prp = problemResultsAll.filter(problem=p)
			result = None
			try:
				result = prp[0]
			except IndexError:
				pass
			problemResults.append(result)


		data = zip(problems, problemResults)
		return render(request, 'program/team/problems.html', {
			'data': data
			})

class ProblemDetailView(View):
	def get(self, request, problemId):
		problem = Problem.objects.get(pk=problemId)
		submissions = ProblemResult.objects.filter(user=request.user, problem=problem)
		return render(request, "program/team/detail.html", 
			{
				'problem' 		: problem,
				'testForm'		: TestForm(),
				'submissions'	: submissions,
				'latestSubmission' : submissions[0] if len(submissions) > 0 else False
			})

	def post(self, request, problemId):
		# Handle file upload
		form = TestForm(request.POST, request.FILES)
		if form.is_valid:
			solution = ProblemSolution(solution=request.FILES['solution'], owner=request.user)
			solution.save()
			return redirect("/program/team/problem/submit/%s?fileId=%s" % (problemId, solution.id))
		return HttpResponseRedirect("index")
		"""
		form = TestForm(request.POST)
		if form.is_valid():
			solution = ProblemSolution(request.POST, request.FILES)
			solution.owner = request.user
			solution.save()
			return HttpResponseRedirect("problems")
		"""
	

class ProblemExecutionView(View):
	def get(self, request, problemId):
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

		solution = ProblemSolution.objects.get(pk=request.GET['fileId'])
		problem = Problem.objects.get(pk=problemId)
		userSettings = UserSettings.objects.get(user=request.user)

		command = userSettings.compiler.getRunCmd(solution.solution)#["python", solution.solution.path]
		osProcess = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		startTime = datetime.datetime.now(tz=timezone(settings.TIME_ZONE))
		stdout, stderr = osProcess.communicate()
		endTime = datetime.datetime.now(tz=timezone(settings.TIME_ZONE))
		#osProcess = ThreadedCommand(["python", solution.solution.path])
		#osProcess.run(5)

		problemResult = ProblemResult(
			submissionTime = startTime,
			successful = False,
			user = request.user,
			problem = problem
			)
		executionResult = ExecutionResult(
			startTime = startTime,
			endTime = endTime,
			stdin = "NOT SUPPORTED",
			stdout = stdout,
			stderr = stderr,
			command = "".join(command),
			exitCode = osProcess.returncode,
			problemResult = problemResult,
			)

		correct = SolutionValidator.validate(problem=problem, executionResult=executionResult)
		problemResult.successful = correct
		problemResult.save()
		executionResult.problemResult = problemResult

		executionResult.save()


		return redirect('problems')



