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

from problems.models import Problem, ProblemResult


logging.basicConfig(filename="django.log", level=logging.CRITICAL)

class UserSettings(DjangoModels.Model):
	user = DjangoModels.OneToOneField(User, primary_key=True)
	teamName = DjangoModels.CharField(max_length=30)

	def score(self):
		problems = Problem.objects.all()
		score = 0
		for problem in problems:
			correct = problem.getCorrectSolution(self.user)
			if(correct):
				score += problem.possibleScore(self.user)
		return score

	def getCorrect(self):
		correct = ProblemResult.objects.filter(user=self.user, graded=True, successful=True)
		problems = [pr.problem for pr in correct]
		return problems

	def getFailed(self):
		problems = Problem.objects.all()
		failed = [pr for pr in problems if pr.failed(self.user)]
		return failed

	def __unicode__(self):
		return ("%s's Settings" % (self.user,))

