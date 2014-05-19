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
			color = "green" if not color else color
			output = output % ("glyphicon-ok", color)
		elif not successful and not pending: # not successful 
			color = "red" if not color else color
			output = output % ("glyphicon-remove", color)
		elif pending: # pending
			color = "rgb(150,150,255)" if not color else color
			output = output % ("glyphicon-question-sign", color)
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