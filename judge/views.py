from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import HttpResponse
from django import forms
import django.contrib.auth.models as auth
from django.conf import settings

from team.models import UserSettings, ProblemResult
from team.library import progressBar

# Create your views here.

class GradingView(View):
	def get(self, request):
		return render(request, "judge/grading.html")

class UserListView(View):
	def get(self, request):
		users = auth.User.objects.filter(is_staff=False)
		return render(request, "judge/user_list.html", {
				'users' : users
			})

class UserDetailView(View):
	def get(self, request, username, userId):
		user = auth.User.objects.get(pk=userId)
		settings = UserSettings.objects.get(user=user)

		results = ProblemResult.objects.filter(user=user)
		correct = len(settings.getCorrect())
		failed = len(settings.getFailed())

		(correctPercent, failedPercent) = progressBar(user)
		total = results.count()
		return render(request, "judge/user_detail.html", {
			'selectedUser'		: user,
			'results'			: results,
			'correct'			: correct,
			'failed'			: failed,
			'correctPercent'	: correctPercent,
			'failedPercent'		: failedPercent,
			'numTotal'			: total
		})
