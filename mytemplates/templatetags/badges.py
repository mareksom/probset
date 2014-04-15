from django import template

register = template.Library()

data = (
	('Very Easy', 'warning', 'veasy'),
	('Easy', 'info', 'easy'),
	('Medium', 'success', 'medium'),
	('Hard', 'important', 'hard'),
	('Very Hard', 'inverse', 'vhard'),

	('Boring', 'warning', 'boring'),
	('Typical', 'info', 'typical'),
	('Not Bad', 'success', 'notbad'),
	('Cool', 'important', 'cool'),
	('Awesome', 'inverse' ,'awesome'),
)

def make_i(i):
	tmp = '<span class="badge badge-{}">{}</span>'.format(data[i][1], data[i][0])
	def fun():
		return tmp
	register.simple_tag(fun, name=data[i][2])

for i in range(5):
	make_i(i)

@register.simple_tag
def difficulty(i, apo = False):
	i = int(i)
	if i < 0 or i > 4:
		raise IndexError
	if apo:
		return "<span class='badge badge-{}'>{}</span>".format(data[i][1], data[i][0])
	return '<span class="badge badge-{}">{}</span>'.format(data[i][1], data[i][0])

@register.simple_tag
def coolness(i, apo = False):
	i = int(i)
	if i < 0 or i > 4:
		raise IndexError
	if apo:
		return "<span class='badge badge-{}'>{}</span>".format(data[i+5][1], data[i+5][0])
	return '<span class="badge badge-{}">{}</span>'.format(data[i+5][1], data[i+5][0])
