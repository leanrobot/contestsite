
from program.models import UserSettings, ContestSettings


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
		siteContext['settings'] = UserSettings.objects.get(user=request.user)

	# Wire in ContestSettings Object
	siteContext['contest'] = ContestSettings.objects.get(pk=1)

	return siteContext




