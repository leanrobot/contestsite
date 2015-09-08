from __future__ import absolute_import

from django.conf.urls import patterns, url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from . import views

urlpatterns = patterns('',
    url(r'^login\/?', views.LoginPage.as_view(), name="login"),
    url(r'^logout\/?', login_required( views.LogoutPage.as_view() ), name="logout"),
)
