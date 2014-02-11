from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings


from datetime import timedelta,datetime

from pytz import timezone


# Create your models here.
class Problem(models.Model):
	name 				= models.CharField(max_length=100)
	score 				= models.IntegerField()

	inputTest			= models.TextField(blank=True)
	outputTest			= models.TextField()

	inputSubmit			= models.TextField(blank=True)
	outputSubmit		= models.TextField()

	description			= models.TextField(blank=True)
	inputDescription	= models.TextField(blank=True)
	outputDescription	= models.TextField(blank=True)

	def __unicode__(self):
		return self.name + " - " + str(self.score) + " points"

class ProblemResult(models.Model):
	class Meta:
		ordering = ['-submissionTime']

	submissionTime 		= models.DateTimeField()
	successful			= models.BooleanField(default=False)
	user 				= models.ForeignKey(User)
	problem 			= models.ForeignKey(Problem)

	def minsAgo(self):
		now = datetime.now(tz=timezone(settings.TIME_ZONE))
		delta = now - self.submissionTime
		minsAgo = delta.total_seconds() /60
		return int(minsAgo)

	#TODO WRITE __UNICODE__
	def __unicode__(self):
		return self.problem.name + " correct? " + unicode(self.successful) + " @ " + unicode(self.submissionTime)

class ProblemScore(models.Model):
	user 			= models.ForeignKey(User)
	problem 		= models.ForeignKey(Problem)
	score 			= models.IntegerField()

	@staticmethod
	def possibleScore(userdata, problem):
		incorrect = ProblemResult.objects.filter(user=userdata.user, problem=problem,
								 successful=False)
		score = problem.score
		score -= len(incorrect) * ContestSettings.objects.get(pk=1).deduction
		return score

class ExecutionResult(models.Model):
	class Meta:
		ordering = ['-startTime']
	startTime			= models.DateTimeField()
	endTime				= models.DateTimeField()
	stdout				= models.TextField()
	stdin				= models.TextField(blank=True)
	stderr				= models.TextField(blank=True)
	command				= models.CharField(max_length=200)
	exitCode			= models.IntegerField()
	problemResult 		= models.OneToOneField(ProblemResult, primary_key=True)

	#TODO WRITE __UNICODE__

def get_uploaded_path(instance, filename):
	return os.path.join(instance.owner.username, filename)

class ProblemSolution(models.Model):
	owner 				= models.ForeignKey(User)
	solution 			= models.FileField(upload_to=get_uploaded_path)

class Compiler(models.Model):
	name 				= models.CharField(max_length=30)
	extension			= models.CharField(max_length=10)
	compiled 			= models.BooleanField()
	compileCmd 			= models.TextField(blank=True)
	runCmd 				= models.TextField()

	def _getCmd(self, commandStr, solutionFile):
		pass
		fullname = solutionFile.path # Testing Phase
		directory = os.path.dirname(solutionFile.path)
		filename = os.path.basename(solutionFile.path)
		basename = os.path.splitext(solutionFile.path)[0]
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

class ContestSettings(models.Model):
	startTime 			= models.DateTimeField()
	endTime 			= models.DateTimeField()
	paused				= models.BooleanField()

	name 				= models.TextField()
	deduction 			= models.IntegerField(default=0)

	def inSession(self, time):
		return self.startTime <= time and time <= self.endTime and not self.paused

	def __unicode__(self):
		return "%s -- Start: %s. End: %s. Paused? %s" % (self.name, self.startTime, self.endTime, self.paused)

class UserSettings(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	teamName = models.CharField(max_length=30)
	compiler = models.ForeignKey(Compiler)
	score = models.IntegerField(default=0)

	def __unicode__(self):
		return ("%s's Settings" % (self.user,))

