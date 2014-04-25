from tastypie.resources import ModelResource
from team.models import ExecutionResult

class UngradedExecutionResultResource(ModelResource):
	class Meta:
		queryset = ExecutionResult.objects.filter(problemResult=None)
		resource_name = "ungradedresult"