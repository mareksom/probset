from django import template

from utils import bbcode

register = template.Library()

@register.tag(name='bbcode')
def do_dialog(parser, token):
	code = parser.parse(('endbbcode',))
	parser.delete_first_token()
	return BBCodeNode(code)

class BBCodeNode(template.Node):
	def __init__(self, code):
		self.code = code
	def render(self, context):
		code = self.code.render(context).strip()
		return bbcode.evaluate(code)
