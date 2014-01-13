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
	problemResult 		= models.ForeignKey(ProblemResult)

	#TODO WRITE __UNICODE__

def get_uploaded_path(instance, filename):
	return os.path.join(instance.owner.username, filename)

class ProblemSolution(models.Model):
	owner = models.ForeignKey(User)
	solution = models.FileField(upload_to=get_uploaded_path)
