from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import HttpResponse
from django import forms
import django.contrib.auth as auth
from django.conf import settings

from team.models import ContestSetting

class ControlView(View):
	def get(self, request):
		contestsettings = ContestSetting.objects.get(pk=1)
		settings = ContestSettingForm(instance=contestsettings)
		#userControl = UserControlForm()
		userCreate = CreateUsersForm()

		return render(request, "control/control.html", {
			"contestSettings" : settings,
			#"userControl"		: userControl,
			"userCreate"		: userCreate,

		})