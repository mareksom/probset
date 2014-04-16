from django.db import models

from django.utils import timezone

from django.contrib.auth.models import User

from tags.models import Tag

class Problem(models.Model):
	user = models.ForeignKey(User)
	author = models.CharField(max_length=100)
	title = models.CharField(max_length=100)
	created_date = models.DateTimeField(auto_now_add=True)
	edited_date = models.DateTimeField(auto_now=True)
	description = models.TextField()
	tags = models.ManyToManyField(Tag)
	difficulty = models.IntegerField()
	coolness = models.IntegerField()

	class Error(Exception):
		title = ''
		author = ''
		difficulty = ''
		coolness = ''
		def is_error(self):
			return self.title != '' or self.author != '' or self.difficulty != '' or self.coolness != ''

	def check(self):
		err = self.Error()
		if not 0 < len(self.title) <= 100:
			err.title = "Title should be a string of length from range [1, 100]."
		if not 0 < len(self.author) <= 100:
			err.author = "Author name should be a string of length from range [1, 100]."
		if not 0 <= self.difficulty <= 4:
			err.difficulty = "Difficulty must be an integer from range [0,4]."
		if not 0 <= self.coolness <= 4:
			err.coolness = "Coolness must be an integer from range [0,4]."
		if err.is_error():
			raise err

	def save(self):
		self.check()
		super(Problem, self).save()

	def __str__(self):
		return "'{}' by {}".format(self.title, self.author)
