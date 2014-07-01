from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import User

class Post(models.Model):
	user = models.ForeignKey(User)
	created_date = models.DateTimeField(auto_now_add=True)
	edited_date = models.DateTimeField(auto_now=True)
	content = models.TextField()

	# One of the fields below should be null, and other should be filled
	answer_to = models.ForeignKey('Post', null=True, blank=True)
	thread = models.ForeignKey('Thread', null=True, blank=True)

	def get_thread(self):
		if self.thread is None:
			if self.answer_to is None:
				return None
			return self.answer_to.get_thread()
		return self.thread

	class Error(Exception):
		content = ''
		def is_error(self):
			return self.content != ''
	
	def check(self):
		err = self.Error()
		if len(self.content) == 0 or self.content.isspace():
			err.content = "The post shall contain at least one non-whitespace character."
		if err.is_error():
			raise err
	
	def update_last_post(self):
		thread = self.get_thread()
		if thread is not None:
			thread.set_last_post(self)
	
	def save(self):
		if self.id is None:
			new_post = True
		else:
			new_post = False

		self.check()
		super(Post, self).save()
		if new_post:
			self.update_last_post()
	
	def __str__(self):
		return "{} wrote {:.10}".format(self.user, self.content)


class Thread(models.Model):
	created_date = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=200)

	last_post = models.ForeignKey('Post', null=True, blank=True, related_name='last_post')

	class Error(Exception):
		title = ''
		def is_error(self):
			return self.title != ''
	
	def check(self):
		err = self.Error()
		if len(self.title) == 0 or self.title.isspace():
			err.title = "The title shall contain at least one non-whitespace character."
		elif len(self.title) > 200:
			err.title = "The title shouldn't be longer than 200 characters."
		if err.is_error():
			raise err
	
	def set_last_post(self, new_last_post):
		self.last_post = new_last_post
		self.save()
	
	def save(self):
		self.check()
		super(Thread, self).save()
	
	def author(self):
		try:
			author_post = self.post_set.get()
		except self.MultipleObjectsReturned:
			return None
		except self.DoesNotExist:
			return None
		return author_post.user
	
	def __str__(self):
		return "Thread: {}".format(self.title)

