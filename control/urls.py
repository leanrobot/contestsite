from __future__ import absolute_import

from django.conf.urls import patterns, include, url
from django.contrib import admin

from control.views import ControlView

urlpatterns = patterns('',
    url(r'^init/$', ControlView.as_view(), name='control-init'),
)

