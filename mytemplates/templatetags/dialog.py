from django import template

register = template.Library()

@register.tag(name='dialog')
def do_dialog(parser, token):
	title = parser.parse(('body',))
	parser.delete_first_token()
	body = parser.parse(('buttons',))
	parser.delete_first_token()
	buttons = parser.parse(('enddialog',))
	parser.delete_first_token()

	try:
		dialog_id = token.split_contents()[1]
	except IndexError:
		dialog_id = 'TO_JEST_BARDZO_ZLE_ID_NALEZY_JE_ZMIENIC'
	try:
		button_text = token.split_contents()[2]
	except IndexError:
		button_text = 'Launch modal'
	try:
		button_class = token.split_contents()[3]
	except IndexError:
		button_class = '"btn"'

	return DialogNode(title, body, buttons, dialog_id, button_class, button_text)

class DialogNode(template.Node):
	def __init__(self, title, body, buttons, dialog_id, button_class, button_text):
		self.title = title
		self.body = body
		self.buttons = buttons
		self.dialog_id = dialog_id
		self.button_class = button_class
		self.button_text = button_text
	def render(self, context):
		title = self.title.render(context)
		body = self.body.render(context)
		buttons = self.buttons.render(context)
		return """
<a href="#{dialog_id}" role="button" class={button_class} data-toggle="modal">{button_text}</a>
<div id="{dialog_id}" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="{dialog_id}Label" aria-hidden="true">
	<div class="modal-header">
		<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
		<h3 id="{dialog_id}Label">{title}</h3>
	</div>
	<div class="modal-body">
		{body}
	</div>
	<div class="modal-footer">
		{buttons}
	</div>
</div>
		""".format(title=title, body=body, buttons=buttons, dialog_id=self.dialog_id, button_class=self.button_class, button_text=self.button_text)
