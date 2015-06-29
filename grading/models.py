from __future__ import absolute_import
import os
from datetime import timedelta,datetime
import logging
import sys

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.query import EmptyQuerySet

from pytz import timezone
from celery.contrib import rdb


# Create your models here.

def fixedTZData(dbDate):
	fixedDate = dbDate.astimezone(timezone(settings.TIME_ZONE))
	return fixedDate

class Compiler(models.Model):
	name 				= models.CharField(max_length=30)
	extension			= models.CharField(max_length=10, unique=True)
	compiled 			= models.BooleanField()
	compileCmd 			= models.TextField(blank=True)
	runCmd 				= models.TextField()

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

class ProblemScore(models.Model):
	user 			= models.ForeignKey(User)
	problem 		= models.ForeignKey('problems.Problem')
	score 			= models.IntegerField()

class ProblemResult(models.Model):
	class Meta:
		ordering = ['-submissionTime']

	submissionTime 		= models.DateTimeField()
	graded				= models.BooleanField(default=settings.AUTO_GRADE)
	successful			= models.BooleanField(default=False)
	user 				= models.ForeignKey(User)
	problem 			= models.ForeignKey('problems.Problem')
	
	def failed(self):
		return self.problem.failed(self.user)

	def minsAgo(self):
		now = datetime.now(tz=timezone(settings.TIME_ZONE))
		delta = now - self.submissionTime
		minsAgo = delta.total_seconds() /60
		return int(minsAgo)

	def prettyTime(self):
		d = fixedTZData(self.submissionTime)
		now = datetime.now(tz=timezone(settings.TIME_ZONE))
		delta = d - now

		sixHours = timedelta(hours=6)
		if delta < sixHours:
			#no date
			return d.strftime("%I:%M %p")
		else:
			return d.strftime("%I:%M %p")
			# print with date

	def __unicode__(self):
		return self.problem.name + " correct? " + unicode(self.successful) + " @ " + unicode(self.submissionTime)

class ProblemSolution(models.Model):
	def get_uploaded_path(instance, filename):
		return os.path.join(instance.owner.username, filename)

	owner 				= models.ForeignKey(User)
	solution 			= models.FileField(upload_to=get_uploaded_path)

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

class ExecutionResult(models.Model):
	class Meta:
		ordering = ['-startTime']
	startTime			= models.DateTimeField()
	endTime				= models.DateTimeField()
	stdout				= models.TextField()
	stdin				= models.TextField(blank=True)
	stderr				= models.TextField(blank=True)
	command				= models.CharField(max_length=200)
	filename 			= models.CharField(max_length=200, blank=True)
	diff 				= models.TextField(blank=True)
	exitCode			= models.IntegerField()
	problemResult 		= models.OneToOneField(ProblemResult, null=True, blank=True)
