import datetime

from django.http import HttpResponseRedirect
from django.conf import settings

from pytz import timezone

from program.models import ContestSettings
import program.views as views

# Test to check if contest is in session
class ContestInSession:
	def process_request(self, request):
		if not request.path.startswith(u"/program/"):
			return None

		contestSettings = ContestSettings.objects.get(pk=1)
		now = datetime.datetime.now(tz=timezone(settings.TIME_ZONE))

		if contestSettings.inSession(now):
			return None
		else:
			return views.WaitView().get(request)