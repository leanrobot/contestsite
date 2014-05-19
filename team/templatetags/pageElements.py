from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter(is_safe=True)
def statusIcon(result, color=False):
	if result:
		successful = result.successful and result.graded
		pending = not result.graded

		output = '<span class="glyphicon %s" style="color: %s"></span>'
		if successful and not pending: # successful
			output = output % ("glyphicon-ok", "green")
		elif not successful and not pending: # not successful 
			output = output % ("glyphicon-remove", "red")
		elif pending: # pending
			output = output % ("glyphicon-question-sign", "rgb(150,150,255)")
		else:
			output = "<span>PR STATUS ERROR</span>"
		return mark_safe(output)

	return mark_safe("<span></span>")

@register.filter()
def statusCSS(result):
	successful = result.successful and result.graded
	pending = not result.graded

	output = ""
	if successful and not pending:
		output = "success"
	if not successful and not pending:
		output = ""
	else:
		pass
	return output

@register.simple_tag
def questionMark():
	return mark_safe('<span class="glyphicon glyphicon-question-sign" style="color:rgb(150,150,255)"></span>')