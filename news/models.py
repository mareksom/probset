from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

from utils import bbcode

class News(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True)
	edited_date = models.DateTimeField(auto_now=True)

	class Error(Exception):
		title = ''
		text = ''
		def is_error(self):
			return self.title != '' or self.text != ''
	
	def clean(self):
		err = self.Error()
		if self.title == '':
			err.title = "Title cannot be empty."
		if self.text == '':
			err.text = "Message cannot be empty."
		if err.is_error():
			raise err

	def __str__(self):
		return '{}: ({}) "{:.10}"'.format(self.user.username, self.title, self.text)
