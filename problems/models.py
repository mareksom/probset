from django.db import models

from django.utils import timezone

from django.contrib.auth.models import User

from tags.models import Tag
from threads.models import Thread

class Problem(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	author = models.CharField(max_length=100)
	title = models.CharField(max_length=100)
	created_date = models.DateTimeField(auto_now_add=True)
	edited_date = models.DateTimeField(auto_now=True)
	description = models.TextField()
	task = models.TextField()
	solution = models.TextField()
	tags = models.ManyToManyField(Tag)
	difficulty = models.IntegerField()
	coolness = models.IntegerField()

	comments = models.ForeignKey(Thread, on_delete=models.CASCADE)

	def is_attached(self):
		return self.round_set.count() > 0
	
	def has_package(self):
		return self.package_set.count() > 0

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
	
	def delete(self):
		for package in self.package_set.all():
			package.delete()
		super(Problem, self).delete()

	def save(self):
		if self.id is None:
			thread = Thread(type='comment')
			thread.save()
			self.comments = thread
		self.check()
		super(Problem, self).save()

	def __str__(self):
		return "'{}' by {}".format(self.title, self.author)
