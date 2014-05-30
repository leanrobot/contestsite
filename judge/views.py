from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import HttpResponse
from django import forms
import django.contrib.auth.models as auth
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator


from django.conf import settings
from django import forms

from team.models import UserSettings, ProblemResult, ExecutionResult
from team.library import progressBar

# Create your views here.

class GradingView(View):
	def get(self, request):
		return render(request, "judge/grading.html")

	@method_decorator(user_passes_test(lambda u: u.is_staff, login_url="/admin"))
	def dispatch(self, *args, **kwargs):
		return super(GradingView, self).dispatch(*args, **kwargs)


class UserListView(View):
	def get(self, request):
		users = auth.User.objects.filter(is_staff=False)
		return render(request, "judge/user_list.html", {
				'users' : users,
			})

	@method_decorator(user_passes_test(lambda u: u.is_staff, login_url="/admin"))
	def dispatch(self, *args, **kwargs):
		return super(UserListView, self).dispatch(*args, **kwargs)

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

	@method_decorator(user_passes_test(lambda u: u.is_staff, login_url="/admin"))
	def dispatch(self, *args, **kwargs):
		return super(UserDetailView, self).dispatch(*args, **kwargs)

class ActionForm(forms.Form):
	action = forms.CharField(max_length=10, widget=forms.HiddenInput)

class ProblemResultDetailView(View):
	def get(self, request, resultId):
		actionForm = ActionForm()
		try:
			pResult = ProblemResult.objects.get(pk=resultId)
		except ProblemResult.DoesNotExist:
			pass #TODO
		problem = pResult.problem
		eResult = ExecutionResult.objects.get(problemResult=pResult)

		return render(request, "judge/problemresult_detail.html", {
			'problem'		: problem,
			'execution'		: eResult,
			'result'		: pResult,
			'form'			: actionForm,
		})

	@method_decorator(user_passes_test(lambda u: u.is_staff, login_url="/admin"))
	def dispatch(self, *args, **kwargs):
		return super(ProblemResultDetailView, self).dispatch(*args, **kwargs)

	def post(self, request, resultId):
		action = request.POST['action']
		result = ProblemResult.objects.get(pk=resultId)
		user = result.user
		if action == "regrade":
			result.graded = False
			result.save()
		elif action == "delete":
			execution = ExecutionResult.objects.get(problemResult=result)
			execution.delete()
			result.delete()
		return redirect('user detail', user.username, user.id)


