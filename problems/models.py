from django.db import models

from grading.models import ProblemResult
from control.models import ContestSettings

inputTypes = (
	('none', 'None'),
	('file', 'File'),
	('stdin', 'Stdin'),
)

# Create your models here.
class Problem(models.Model):
	name 				= models.CharField(max_length=100)
	score 				= models.IntegerField()

	inputType 			= models.CharField(max_length=5, choices=inputTypes)
	filename			= models.CharField(max_length=30, blank=True)
	inputTest			= models.TextField(blank=True)
	outputTest			= models.TextField()

	inputSubmit			= models.TextField(blank=True)
	outputSubmit		= models.TextField()

	description			= models.TextField(blank=True)
	inputDescription	= models.TextField(blank=True)
	outputDescription	= models.TextField(blank=True)

	def getCorrectSolution(self, user):
		correctResults = ProblemResult.objects.filter(user=user, problem=self, successful=True, graded=True)
		if(correctResults.count() > 0):
			return correctResults.first()
		return None

	def getIncorrectSolutions(self, user):
		incorrectResults = ProblemResult.objects.filter(user=user, problem=self, successful=False, graded=True)
		if(len(incorrectResults > 0)):
			return incorrectResults
		return None

	def latestSubmission(self, user):
		latest = ProblemResult.objects.filter(user=user, problem=self).first()
		return latest


	def possibleScore(self, user):
		incorrect = ProblemResult.objects.filter(user=user, problem=self,
								 successful=False, graded=True)
		score = self.score
		score -= len(incorrect) * ContestSettings.objects.get(pk=1).deduction
		return score if score >=0 else 0

	def failed(self, user):
		return self.possibleScore(user) <= 0

	def __unicode__(self):
		return self.name + " - " + str(self.score) + " points"