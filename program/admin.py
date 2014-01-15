from django.contrib import admin
from program.models import *

# Register your models here.
admin.site.register(Problem)
admin.site.register(ProblemResult)
admin.site.register(ExecutionResult)
admin.site.register(ProblemSolution)
admin.site.register(Compiler)
admin.site.register(UserSettings)
admin.site.register(ContestSettings)
