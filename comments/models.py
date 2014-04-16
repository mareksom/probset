from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import User

from problems.models import Problem

class Comment(models.Model):
	user = models.ForeignKey(User)
	created_date = models.DateTimeField(auto_now_add=True)
	edited_date = models.DateTimeField(auto_now=True)
	comment = models.TextField()
	problem = models.ForeignKey(Problem)

	class Error(Exception):
		comment = ''
		def is_error(self):
			return self.comment != ''

	def check(self):
		err = self.Error()
		if len(self.comment) == 0:
			err.comment = "Comment shall not be empty."
		if err.is_error():
			raise err

	def save(self):
		self.check()
		super(Comment, self).save()

	def __str__(self):
		return "{} wrote {:.10}".format(self.user, self.comment)
