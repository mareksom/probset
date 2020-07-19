from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import User

from threads.models import Thread

class ForumThread(models.Model):
	created_date = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=200)
	thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

	class Error(Exception):
		title = ''
		def is_error(self):
			return self.title != ''
	
	def clean(self):
		err = self.Error()
		if len(self.title) == 0 or self.title.isspace():
			err.title = "The title shall contain at least one non-whitespace character."
		elif len(self.title) > 200:
			err.title = "The title shouldn't be longer than 200 characters."
		if err.is_error():
			raise err
	
	def save(self):
		if self.id is None:
			thread = Thread(type='forum')
			thread.save()
			self.thread = thread
		super(ForumThread, self).save()
	
	def __str__(self):
		return "ForumThread: {}".format(self.title)

