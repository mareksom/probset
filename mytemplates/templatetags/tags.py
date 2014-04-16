from django import template

register = template.Library()

@register.simple_tag
def textcolor(color):
	r = int(color[1:3],16)
	g = int(color[3:5],16)
	b = int(color[5:7],16)
	if (r+g+b) > (255*3)/2: return '#000'
	return '#fff'

@register.simple_tag
def puttag(tag, color = False, apo = False, full=False):
	if color:
		text = tag.color
		title = ''
	else:
		if full:
			text = tag.name
		else:
			text = tag.short
		title = tag.name
	if apo:
		string = "<span title='{}' class='label' style='background-color: {}; color: {};'>{}</span>"
	else:
		string = '<span title="{}" class="label" style="background-color: {}; color: {};">{}</span>'
	return string.format(title, tag.color, textcolor(tag.color), text)
