from __future__ import absolute_import

from django.contrib import admin
from .models import *

from solo.admin import SingletonModelAdmin

# Register your models here.
admin.site.register(Problem)
admin.site.register(ProblemResult)
admin.site.register(ExecutionResult)
admin.site.register(ProblemSolution)
admin.site.register(Compiler)
admin.site.register(UserSettings)
admin.site.register(ContestSetting, SingletonModelAdmin)
