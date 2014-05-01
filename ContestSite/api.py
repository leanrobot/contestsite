from tastypie.resources import ModelResource
from tastypie import fields
from team.models import ExecutionResult, ProblemResult, Problem

class ProblemResource(ModelResource):
	class Meta:
		queryset = Problem.objects.all()

class ExecutionResultResource(ModelResource):
	class Meta:
		queryset = ExecutionResult.objects.all()

class UngradedResultResource(ModelResource):
	problem = fields.OneToOneField(ProblemResource, 'problem', full=True)
	execution = fields.OneToOneField(ExecutionResultResource, 'executionresult', full=True)
	class Meta:
		queryset = ProblemResult.objects.filter(graded=False)
		resource_name = "ungradedresult"
