from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import HttpResponse
from django import forms
import django.contrib.auth.models as auth
from django.conf import settings

from team.models import UserSettings

# Create your views here.

class GradingView(View):
	def get(self, request):
		return render(request, "judge/grading.html")

class UserDetailView(View):
	def get(self, request, username):
		users = auth.User.objects.filter(is_staff=False)
		return render(request, "judge/user_detail.html", {
				'users' : users
			})
