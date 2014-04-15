from postmarkup import create, TagBase, SimpleTag

import re

include_list = (
	'b', 'i', 'u', 's', 'size', 'color', 'center', 'url', 'quote', 'code', 'img', 'list', '*', 'latex',
)

class LatexTag(TagBase):
	def __init__(self, name):
		super(LatexTag, self).__init__(name, enclosed=True, inline=True)
	
	def render_open(self, parser, node_index):
		contents = self.get_contents(parser)
		self.skip_contents(parser)
		return r'\[{}</latex>\]'.format(contents)

my_bbcode = create(include = include_list, annotate_links = False)
my_bbcode.add_tag(LatexTag, 'latex')
render_bbcode = my_bbcode.render_to_html

def evaluate(text):
	return '<div class="bbcode">' + render_bbcode(text) + '</div>'
