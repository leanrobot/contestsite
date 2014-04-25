from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import HttpResponse
from django import forms
import django.contrib.auth as auth
from django.conf import settings

# Create your views here.

class GradingView(View):
	def get(self, request):
		return render(request, "judge/grading.html")
