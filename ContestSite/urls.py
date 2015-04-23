from __future__ import absolute_import

from django.conf.urls import patterns, include, url
from django.contrib import admin

from tastypie.api import Api
from .api import *
from team.views import ScoreboardView

admin.autodiscover()

v1_api = Api(api_name="v1")
v1_api.register(UngradedResultResource())
v1_api.register(ExecutionResultResource())
v1_api.register(ProblemResource())
v1_api.register(ProblemResultResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ContestSite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', ScoreboardView.as_view(), name='index'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^control/', include('control.urls')),
    url(r'^team/', include('team.urls')),
    url(r'^judge/', include('judge.urls')),
    url(r'^api/', include(v1_api.urls)),
)
