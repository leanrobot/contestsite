from django.conf import settings

from program.models import UserSettings, ContestSettings, ProblemResult

from pytz import timezone



class SolutionValidator:
	@staticmethod
	def validate(problem, executionResult):
		exitCodeCorrect = executionResult.exitCode == 0
		stdoutMatch = SolutionValidator._compareStdout(executionResult.stdout, problem.outputSubmit)

		return exitCodeCorrect and stdoutMatch

	@staticmethod
	def _compareStdout(actual, expected):
		cleanActual = unicode(actual.replace("\r", u""))
		cleanExpected = unicode(expected.replace("\r", u""))
		returnVal = cleanActual == cleanExpected
		return returnVal

# Site-wide Context Processor
def programSiteContext(request):
	siteContext = {}

	# Wire in UserSettings Object
	if request.user.is_authenticated():
		try:
			siteContext['userdata'] = UserSettings.objects.get(user=request.user)
		except UserSettings.DoesNotExist:
			pass

	# Wire in ContestSettings Object
	siteContext['contest'] = ContestSettings.objects.get(pk=1)

	#wire contest end time
	siteContext['contestEndTimestamp'] = siteContext['contest'].endTime.astimezone(timezone(settings.TIME_ZONE)).isoformat()

	return siteContext




