from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def icon(name, white = False):
	if white:
		white_str = ' icon-white'
	else:
		white_str = ''
	return format_html('<i class="icon icon-{}{}"></i>', name, white_str)
