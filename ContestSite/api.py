from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import BasicAuthentication
from tastypie.resources import ModelResource
from tastypie import fields

from grading.models import ExecutionResult, ProblemResult
from problems.models import Problem

class ProblemResource(ModelResource):
	class Meta:
		queryset = Problem.objects.all()

class ExecutionResultResource(ModelResource):

	class Meta:
		queryset = ExecutionResult.objects.all()

class UngradedResultResource(ModelResource):
	problem = fields.OneToOneField(ProblemResource, 'problem', full=True)
	execution = fields.OneToOneField(ExecutionResultResource, 'executionresult', full=True)
	time = fields.CharField(attribute='prettyTime', readonly=True)
	minsAgo = fields.IntegerField(attribute='minsAgo', readonly=True)
	team = fields.CharField(readonly=True)

	def dehydrate(self, bundle):
		bundle.data['team'] = bundle.obj.user.username
		return bundle

	class Meta:
		queryset = ProblemResult.objects.filter(graded=False)
		resource_name = "ungradedresult"
		authorization = DjangoAuthorization()

class ProblemResultResource(ModelResource):
	class Meta:
		queryset = ProblemResult.objects.all()
		resource_name = "problemresult"
		authorization = DjangoAuthorization()
