import datetime
#from datetime.datetime import now

from django.shortcuts import render
from django.core.urlresolvers import resolve

from team.models import ContestSetting
from control.views import ControlView

class ContestSettingMiddlware:
	""" Ensure that a ContestSetting exists for the competition
	""" 
	def process_view(request, process_request):
		exists = ContestSetting.objects.all().exists()

		# allow users to view the page where they may set the settings
		if exists or resolve(request.path) == "control-init":
			return None

		return ControlView().get(request)






