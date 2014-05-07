from __future__ import absolute_import

from django.conf.urls import patterns, url


from . import views

urlpatterns = patterns('',
	url(r'^grade/?$\/?', views.GradingView.as_view() , name="grading"),
	url(r'^user/(\w+)\/?', views.UserDetailView.as_view(), name="grading")


)