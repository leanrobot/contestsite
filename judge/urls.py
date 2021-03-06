from __future__ import absolute_import

from django.conf.urls import patterns, url


from . import views

urlpatterns = patterns('',
	url(r'^grade/?$\/?', views.GradingView.as_view() , name="grading"),
	url(r'^user\/?$', views.UserListView.as_view(), name="user list"),
	url(r'^user/(\w+)/(\d+)\/?', views.UserDetailView.as_view(),
		name="user detail"),
	url(r'^result/(\d+)\/?', 
		views.ProblemResultDetailView.as_view(), name="problem result detail"),
	url(r'^control\/?', views.ControlView.as_view(), name="contest control"),



)