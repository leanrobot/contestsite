from __future__ import absolute_import

import django.contrib.auth as auth
from django.shortcuts import render, redirect
from django.views.generic.base import View

class ExecutionAdministration(View):
	def get(self, request):
		return render(request, "program/judge/execution_admin.html", {})