from django.conf.urls import patterns, url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from program import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'^login/', AuthenticationForm.as_view, name="login page")
    url(r'^login/', views.LoginPage.as_view(), name="login"),
    url(r'^logout/', views.LogoutPage.as_view(), name="logout"),

    url(r'problem/$', login_required( views.TeamProblemPage.as_view() ), name="problems"),
    url(r'problem/(\d+)$', views.ProblemDetailView.as_view(), name="problem detail"),
    url(r'problem/submit/(\d+)', views.ProblemExecutionView.as_view(), name="problem execution")
)