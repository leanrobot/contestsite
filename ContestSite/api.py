from tastypie.resources import ModelResource
from team.models import ExecutionResult

class ExecutionResultResource(ModelResource):
	class Meta:
		queryset = ExecutionResult.objects.all()
		resource_name = "executionresult"