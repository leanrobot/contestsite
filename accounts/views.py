from django.shortcuts import render
from django.conf import settings
from django import forms
from django.views.generic.base import View
from django.core.exceptions import PermissionDenied
import django.contrib.auth as auth
from django.shortcuts import render, redirect


class LoginForm(forms.Form):
    username    = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter username'}))
    password    = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter password'}))
    next        = forms.CharField(widget=forms.HiddenInput)

class LoginPage(View):
    def get(self, request):
        loginForm = LoginForm()
        redirect_url = "index"
        if 'next' in request.GET:
            redirect_url = request.GET['next']
        loginForm.fields['next'].initial = redirect_url

        if request.user.is_authenticated():
            return redirect(redirect_url)
        else:
            return render(request, 'program/accounts/login.html', 
                {'form':LoginForm()})

    def post(self, request):
        response = redirect("index")

        if not request.user.is_authenticated():
            usernm = request.POST['username']
            passwd = request.POST['password']
            user = auth.authenticate(username=usernm, password=passwd)

            response = redirect('login')
            if user is not None and user.is_active:
                auth.login(request, user)
                if request.POST['next']:
                    response = redirect(request.POST['next'])

        return response
# ============

class LogoutPage(View):
    def get(self, request):
        auth.logout(request)

        redirectUrl = 'index'
        if 'next' in request.GET:
            redirectUrl = request.GET['next']

        return redirect(redirectUrl)
# ============

class TeamLoginRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        # only staff and teams satisfy the mixin dispatch.
        if not self.is_team_user(user):
            raise PermissionDenied

        return super(TeamLoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)

    def is_team_user(self, user):
        is_team = user.groups.filter(name=settings.TEAM_GROUP_NAME).exists()
        return (is_team and not user.is_anonymous()) or user.is_staff

class JudgeLoginRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user


        # only staff and teams satisfy the mixin dispatch.
        if not self.is_judge_user(user):
            raise PermissionDenied

        return super(JudgeLoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)

    def is_judge_user(self, user):
        is_judge = user.groups.filter(name=settings.JUDGE_GROUP_NAME).exists()
        return (is_judge and not user.is_anonymous()) or user.is_staff