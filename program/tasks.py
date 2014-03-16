from __future__ import absolute_import
import os
import subprocess
from datetime import datetime

from celery import Celery
from pytz import timezone

from django.conf import settings

from .models import UserSettings, ProblemResult, ExecutionResult, ProblemScore
from .library import SolutionValidator, TimeoutThread

#from django.conf import settings
#settings.configure()
'''
from django.core.exceptions import ImproperlyConfigured
from django.contrib.sites.models import Site
'''

#from .models import Problem

worker = Celery('worker', broker='amqp://guest@localhost//')
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ContestSite.settings')

#worker.config_from_object('django.conf:settings')
#worker.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@worker.task
def createProblem(problem):
	pass
	#settings.configure()
	problem.save()
	#'''
	
	#'''

@worker.task
def testSolution(problem, user, solution):
	TIMEOUT = 5

	pass
	userSettings = UserSettings.objects.get(user=user)
	command = userSettings.compiler.getRunCmd(solution.solution)#["python", solution.solution.path]
	#osProcess = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	osProcess = TimeoutThread(["python", solution.solution.path])

	tz = timezone(settings.TIME_ZONE)
	startTime = datetime.now(tz=tz)
	osProcess.run(TIMEOUT)
	#stdout, stderr = osProcess.communicate(input=problem.inputSubmit)
	endTime = datetime.now(tz=tz)

	if osProcess.terminated:
		stdout = "<<<< NO OUTPUT: THE COMMAND TIMED OUT. MORE THAN %i SECONDS TO RUN >>>" % (TIMEOUT)
		stderr = stdout
	else:
		stdout = osProcess.stdout
		stderr = osProcess.stderr
	

	problemResult = ProblemResult(
		submissionTime = startTime,
		successful = False,
		user = user,
		problem = problem
		)
	executionResult = ExecutionResult(
		startTime = startTime,
		endTime = endTime,
		stdin = problem.inputSubmit,
		stdout = stdout,
		stderr = stderr,
		command = " ".join(command),
		exitCode = osProcess.exitCode,
		problemResult = problemResult,
		)

	correct = SolutionValidator.validate(problem=problem, executionResult=executionResult)
	problemResult.successful = correct
	problemResult.save()
	executionResult.problemResult = problemResult
	executionResult.save()

	# Update the user's score if correct
	if correct:
		userSettings.score += ProblemScore.possibleScore(userSettings, problem)
		userSettings.save()


