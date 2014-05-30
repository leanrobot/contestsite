from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import HttpResponse
from django import forms
import django.contrib.auth.models as auth
import django.contrib.auth.hashers as hasher
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

from random import randint

from django.conf import settings
from django import forms

from team.models import UserSettings, ProblemResult, ExecutionResult, ContestSettings
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

class ContestSettingsForm(forms.ModelForm):
	class Meta:
		model = ContestSettings
		fields = ['startTime', 'endTime', 'paused']

class CreateUsersForm(forms.Form):
	userCount = forms.IntegerField(widget=forms.TextInput(attrs={"size":"3"}))


class ControlView(View):
	def get(self, request):
		contestsettings = ContestSettings.objects.get(pk=1)
		settings = ContestSettingsForm(instance=contestsettings)
		#userControl = UserControlForm()
		userCreate = CreateUsersForm()

		return render(request, "judge/control.html", {
			"contestSettings" : settings,
			#"userControl"		: userControl,
			"userCreate"		: userCreate,

		})

	def post(self, request):
		# contestupdate, createusers, cleardata
		action = request.GET['action']
		if action == "contestupate":
			settingsForm = ContestSettingsForm(request.POST)
			if settingsForm.is_valid():
				settingsForm.save()
			pass
		elif action == "createusers":
			pass
			userForm = CreateUsersForm(request.POST)
			userCount = int(userForm.data['userCount'])
			teamGroup = auth.Group.objects.get(name="Team")
			newUsers = []
			for i in range(userCount):
				username = "team%i" % (i+1)
				password = self.choosePassword()
				user = auth.User(username=username, password=hasher.make_password(password))
				user.save()
				teamGroup.user_set.add(user)
				row = (username, password)
				newUsers.append(row)
			teamGroup.save()
			return render(request, "judge/newUsers.html", {
				"users" : newUsers,
			})
		elif action == "cleardata":
			# delete all problem results
			ProblemResult.objects.all().delete()
			# delete all execution results
			ExecutionResult.objects.all().delete()
			# delete all users in group "Team"
			teamGroup = auth.Group.objects.get(name="Team")
			for user in teamGroup.user_set.all():
				user.delete()
			teamGroup.user_set.clear()
			teamGroup.save()
		return redirect('contest control')

	def choosePassword(self):
		choices = ["addle", "addle", "addle", "adieu", "adios", "adits", 
			"adman", "admen", "admit", "admix", "adobe", "adobo",
			"adopt", "adore", "adorn", "adown", "adoze", "adult", 
			"adunc", "adust", "adyta", "adzed", "adzes", "aecia",
			"aedes", "aegis", "aeons", "aerie", "afars", "affix", 
			"afire", "afoot", "afore", "afoul", "afrit", "after",
			"again", "agama", "agape", "agars", "agate", "agave", 
			"agaze", "agene", "agent", "agers", "agger", "aggie",
			"aggro", "aghas", "agile", "aging", "agios", "agism", 
			"agist", "agita", "aglee", "aglet", "agley", "aglow",
			"agmas", "agone", "agons", "agony", "agora", "agree",
			 "agria", "agues", "ahead", "ahing", "ahold", "ahull",
			"aided", "aider", "aides", "ailed", "aimed", "aimer",
			 "aioli", "aired", "airer", "airns", "airth", "airts",
			"aisle", "aitch", "aiver", "ajiva", "ajuga", "akees", 
			"akela", "akene", "alack", "alamo", "aland", "alane",]
		choice = choices[randint(0, len(choices)-1)]
		return choice

	@method_decorator(user_passes_test(lambda u: u.is_staff, login_url="/admin"))
	def dispatch(self, *args, **kwargs):
		return super(ControlView, self).dispatch(*args, **kwargs)


