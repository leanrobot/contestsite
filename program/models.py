from __future__ import absolute_import
import os
from datetime import timedelta,datetime
import logging
import sys

from django.db import models as DjangoModels
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.query import EmptyQuerySet

from pytz import timezone
from celery.contrib import rdb


# Create your models here.
inputTypes = (
	('none', 'None'),
	('file', 'File'),
	('stdin', 'Stdin'),
)

logging.basicConfig(filename="django.log", level=logging.CRITICAL)


class Problem(DjangoModels.Model):
	name 				= DjangoModels.CharField(max_length=100)
	score 				= DjangoModels.IntegerField()

	inputType 			= DjangoModels.CharField(max_length=5, choices=inputTypes)
	filename			= DjangoModels.CharField(max_length=30, blank=True)
	inputTest			= DjangoModels.TextField(blank=True)
	outputTest			= DjangoModels.TextField()

	inputSubmit			= DjangoModels.TextField(blank=True)
	outputSubmit		= DjangoModels.TextField()

	description			= DjangoModels.TextField(blank=True)
	inputDescription	= DjangoModels.TextField(blank=True)
	outputDescription	= DjangoModels.TextField(blank=True)

	def getCorrectSolution(self, user):
		correctResults = ProblemResult.objects.filter(user=user, problem=self, successful=True)
		if(correctResults.count() > 0):
			return correctResults.first()
		return None

	def getIncorrectSolutions(self, user):
		incorrectResults = ProblemResult.objects.filter(user=user, problem=self, successful=False)
		if(len(incorrectResults > 0)):
			return incorrectResults
		return None

	def possibleScore(self, user):
		incorrect = ProblemResult.objects.filter(user=user, problem=self,
								 successful=False)
		score = self.score
		score -= len(incorrect) * ContestSettings.objects.get(pk=1).deduction
		return score

	def __unicode__(self):
		return self.name + " - " + str(self.score) + " points"

class ProblemResult(DjangoModels.Model):
	class Meta:
		ordering = ['-submissionTime']

	submissionTime 		= DjangoModels.DateTimeField()
	successful			= DjangoModels.BooleanField(default=False)
	user 				= DjangoModels.ForeignKey(User)
	problem 			= DjangoModels.ForeignKey(Problem)

	def minsAgo(self):
		now = datetime.now(tz=timezone(settings.TIME_ZONE))
		delta = now - self.submissionTime
		minsAgo = delta.total_seconds() /60
		return int(minsAgo)

	#TODO WRITE __UNICODE__
	def __unicode__(self):
		return self.problem.name + " correct? " + unicode(self.successful) + " @ " + unicode(self.submissionTime)

class ProblemScore(DjangoModels.Model):
	user 			= DjangoModels.ForeignKey(User)
	problem 		= DjangoModels.ForeignKey(Problem)
	score 			= DjangoModels.IntegerField()

class ExecutionResult(DjangoModels.Model):
	class Meta:
		ordering = ['-startTime']
	startTime			= DjangoModels.DateTimeField()
	endTime				= DjangoModels.DateTimeField()
	stdout				= DjangoModels.TextField()
	stdin				= DjangoModels.TextField(blank=True)
	stderr				= DjangoModels.TextField(blank=True)
	command				= DjangoModels.CharField(max_length=200)
	exitCode			= DjangoModels.IntegerField()
	problemResult 		= DjangoModels.OneToOneField(ProblemResult, primary_key=True)

	#TODO WRITE __UNICODE__

def get_uploaded_path(instance, filename):
	return os.path.join(instance.owner.username, filename)

class ProblemSolution(DjangoModels.Model):
	owner 				= DjangoModels.ForeignKey(User)
	solution 			= DjangoModels.FileField(upload_to=get_uploaded_path)

	def getFullName(self):
		return self.solution.path
	def getFilePath(self):
		return os.path.dirname(self.solution.path)
	def getFileName(self):
		return os.path.basename(self.solution.path)
	def getBaseName(self):
		filename = self.getFileName()
		(base, extension) = filename.split(".")
		return base
	def getExtension(self):
		filename = self.getFileName()
		(base, ext) = filename.split(".")
		return ext

	def compiler(self):
		compiler = Compiler.objects.get(extension=self.getExtension())
		return compiler



class Compiler(DjangoModels.Model):
	name 				= DjangoModels.CharField(max_length=30)
	extension			= DjangoModels.CharField(max_length=10, unique=True)
	compiled 			= DjangoModels.BooleanField()
	compileCmd 			= DjangoModels.TextField(blank=True)
	runCmd 				= DjangoModels.TextField()

	def _getCmd(self, commandStr, solutionFile):
		fullname = solutionFile.path # Testing Phase
		directory = os.path.dirname(fullname)
		filename = os.path.basename(fullname)
		basename = os.path.splitext(filename)[0]
		command = commandStr.split(' ')
		def replace(c):
			c = c.replace('{{fullname}}', fullname) 	# /Users/test/programming/test.py
			c = c.replace('{{filename}}', filename)		# test.py
			c = c.replace('{{directory}}', directory)	# /Users/test/programming
			c = c.replace('{{basename}}', basename)		# test
			return c


		return	map(replace, command)

	def getCompileCmd(self, solutionFile):
		return self._getCmd(self.compileCmd, solutionFile)
	def getRunCmd(self, solutionFile):
		return self._getCmd(self.runCmd, solutionFile)

	def __unicode__(self):
		return self.name

class ContestSettings(DjangoModels.Model):
	startTime 			= DjangoModels.DateTimeField()
	endTime 			= DjangoModels.DateTimeField()
	paused				= DjangoModels.BooleanField()

	name 				= DjangoModels.TextField()
	deduction 			= DjangoModels.IntegerField(default=0)

	def inSession(self, time):
		return self.startTime <= time and time <= self.endTime and not self.paused

	def __unicode__(self):
		return "%s -- Start: %s. End: %s. Paused? %s" % (self.name, self.startTime, self.endTime, self.paused)

class UserSettings(DjangoModels.Model):
	user = DjangoModels.OneToOneField(User, primary_key=True)
	teamName = DjangoModels.CharField(max_length=30)
	compiler = DjangoModels.ForeignKey(Compiler)

	def score(self):
		problems = Problem.objects.all()
		score = 0
		for problem in problems:
			correct = problem.getCorrectSolution(self.user)
			if(correct):
				score += problem.possibleScore(self.user)
		return score

	def __unicode__(self):
		return ("%s's Settings" % (self.user,))

