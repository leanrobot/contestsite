from django.db import models
from django.contrib.auth.models import User
import os

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

	#TODO WRITE __UNICODE__
	def __unicode__(self):
		return self.problem.name + " correct? " + unicode(self.successful) + " @ " + unicode(self.submissionTime)

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
	compiled 			= models.BooleanField()
	compileCmd 			= models.TextField(blank=True)
	runCmd 				= models.TextField()

	def _getCmd(self, commandStr, solutionFile):
		pass
		full = solutionFile.path # Testing Phase
		directory = os.path.dirname(solutionFile.path)
		filename = os.path.basename(solutionFile.path)
		basename = os.path.splitext(solutionFile.path)[0]
		command = commandStr.split(' ')
		def replace(c):
			c = c.replace('{{fullname}}', full)
			c = c.replace('{{filename}}', filename)
			c = c.replace('{{directory}}', directory)
			c = c.replace('{{basename}}', basename)
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

	def __unicode__(self):
		return ("%s's Settings" % (self.user,))

