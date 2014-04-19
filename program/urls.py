from __future__ import absolute_import

from django.conf.urls import patterns, url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from .views import TeamViews, JudgeViews

urlpatterns = patterns('',
    url(r'^$', login_required( TeamViews.ScoreboardView.as_view() ), name='index'),

    url(r'judge$', JudgeViews.ExecutionAdministration.as_view(), name="execution admin"),


    url(r'^login/', TeamViews.LoginPage.as_view(), name="login"),
    url(r'^logout/', login_required( TeamViews.LogoutPage.as_view() ), name="logout"),
    url(r'^settings/', login_required( TeamViews.UserSettingsView.as_view() ), name="user settings"),

    url(r'problem/$', login_required( TeamViews.ProblemListView.as_view() ), name="problems"),
    url(r'problem/(\d+)$', login_required( TeamViews.ProblemDetailView.as_view() ), name="problem detail"),
    url(r'problem/(\d+)/view/(\d+)$', login_required( TeamViews.ProblemResultView.as_view() ), name="problem result"),
    url(r'problem/(\d+)/submit/(\d+)$', login_required( TeamViews.ProblemExecutionView.as_view() ), name="problem execution"),
    url(r'problem/(\d+)/file$', login_required( TeamViews.TextFileGeneratorView.as_view() ), name="text file generator"),

    # test view & template
    url(r'test$', TeamViews.TestView.as_view(), name="test"),

    # JUDGE VIEWS =================================================
)



