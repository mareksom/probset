from django import template

register = template.Library()

@register.simple_tag
def icon(name, white = False):
	if white:
		white_str = ' icon-white'
	else:
		white_str = ''
	return '<i class="icon icon-{}{}"></i>'.format(name, white_str)
