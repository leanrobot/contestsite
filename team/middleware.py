from __future__ import absolute_import

import datetime

from django.http import HttpResponseRedirect
from django.conf import settings as djangoSettings
from django.shortcuts import redirect

from pytz import timezone

from .models import ContestSetting, UserSettings
from . import views


# Test to check if contest is in session
class ContestSiteMiddleware:
	def process_request(self, request):
		# whitelist the 'program' root, so as to note disallow /admin/ access. 
		if not request.path.startswith(u"/team/"):
			return None

		# Redirect to the user settings page if the user does not have an associate UserSettings object
		if not (request.path.startswith(u"/team/settings") or request.path.startswith(u"/team/logout")) and request.user.is_authenticated():
			try:
				settings = UserSettings.objects.get(user=request.user)
			except UserSettings.DoesNotExist:
				return redirect('user settings')

		# Check to make sure the contest is in session
		contestSettings = ContestSetting.objects.get(pk=1)
		now = datetime.datetime.now(tz=timezone(djangoSettings.TIME_ZONE))

		if contestSettings.inSession(now):
			return None
		else:
			return views.WaitView().get(request)
