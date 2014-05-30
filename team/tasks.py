from __future__ import absolute_import
import os
import sys
import subprocess
from datetime import datetime
from difflib import unified_diff,ndiff

from celery import Celery
from pytz import timezone

from django.conf import settings

from .models import UserSettings, ProblemResult, ExecutionResult, ProblemScore
from .library import SolutionValidator, TimeoutThread

worker = Celery('worker', broker='amqp://guest@localhost//')
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ContestSite.settings')

#worker.config_from_object('django.conf:settings')
#worker.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@worker.task
def testSolution(problem, user, prResult, exResult, solution):
	TIMEOUT = 5 # CONST VALUE

	userSettings = UserSettings.objects.get(user=user)
	#compileCommand = userSettings.compiler.getCompileCmd(solution.solution)
	command = userSettings.compiler.getRunCmd(solution.solution)#["python", solution.solution.path]
	#osProcess = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	#osProcess = TimeoutThread(["python", solution.solution.path])

	validator = SolutionValidator(problem, solution)

	tz = timezone(settings.TIME_ZONE)
	startTime = datetime.now(tz=tz)
	sys.stderr.write("validate....")
	validator.execute()
	sys.stderr.write("done!\n")
	#osProcess.run(TIMEOUT)
	#stdout, stderr = osProcess.communicate(input=problem.inputSubmit)
	endTime = datetime.now(tz=tz)

	osProcess = validator.thread

	if osProcess.timeout:
		stdout = "<<<< NO OUTPUT: THE COMMAND TIMED OUT. MORE THAN %i SECONDS TO RUN >>>" % (TIMEOUT)
		stderr = stdout
		diff = ''
	else:
		stdout = osProcess.stdout
		stderr = osProcess.stderr

		def unifyDiffArray(arr):
			arr = [x.rstrip() for x in arr]
			unified = "\n".join(arr)
		diff = [x for x in unified_diff(problem.outputSubmit.splitlines(),stdout.splitlines(),
					 tofile="expected", fromfile="stdout")]
		diff = [x.rstrip() for x in diff]
		diff = "\n".join(diff)
	command = " ".join(validator.command)
	command = ("%s\n%s") % (" ".join(validator.compileCommand), command)

	problemResult = prResult
	problemResult.submissionTime = startTime
	problemResult.successful = False
	problemResult.user = user
	problemResult.problem = problem
	problemResult.save()

	executionResult = exResult
	executionResult.startTime = startTime
	executionResult.endTime = endTime
	executionResult.stdin = problem.inputSubmit
	executionResult.stdout = stdout
	executionResult.stderr = stderr
	executionResult.diff = diff
	executionResult.filename = solution.solution.path
	executionResult.command = "%s \n %s" % (" ".join(validator.compileCommand), " ".join(validator.command))
	executionResult.exitCode = osProcess.exitCode
	executionResult.problemResult = problemResult

	correct = validator.validate(problem=problem, executionResult=executionResult)
	problemResult.successful = correct
	problemResult.save()

	#executionResult.problemResult = problemResult
	executionResult.save()

	# Cleanup after executing the solution
	fileField = solution.solution
	fileField.delete()
	solution.delete()
