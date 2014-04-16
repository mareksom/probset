from django.db import models

import re

class Tag(models.Model):
	name = models.CharField(max_length = 100)
	short = models.CharField(max_length = 5)
	color = models.CharField(max_length = 7)

	class Error(Exception):
		name = ''
		short = ''
		color = ''
		def is_error(self):
			return self.name != '' or self.short != '' or self.color != ''
	
	def check(self):
		err = self.Error()

		if len(self.name) > 100:
			err.name = "Tag name is too long (max 100 characters)."
		elif self.name == '':
			err.name = "Tag name cannot be empty."

		if len(self.short) > 5:
			err.short = "Tag short name is too long (max 5 characters)."
		if self.short == '':
			err.short = "Tag short name cannot be empty."

		if re.search(r'^#[0-9A-F]{6}$', self.color) is None:
			err.color = "Color should be in format #RRGGBB."

		if err.is_error():
			raise err

	def save(self):
		self.check()
		super(Tag, self).save()

	def __str__(self):
		return '{} "{}"'.format(self.short, self.name)
