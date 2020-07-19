from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import User

class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	created_date = models.DateTimeField(auto_now_add=True)
	edited_date = models.DateTimeField(auto_now=True)
	content = models.TextField()

	# One of the fields below should be null, and other should be filled
	answer_to = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True)
	thread = models.ForeignKey('Thread', on_delete=models.CASCADE, null=True, blank=True)

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
		return "{} wrote {:.30}".format(self.user, self.content)


class Thread(models.Model):
	last_post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True, related_name='last_post')
	type = models.CharField(max_length=10)
	seen_by = models.ManyToManyField(User)

	def events(self):
		event_list = []
		def add_post(post):
			nonlocal event_list
			event_list += [post]
			if post.post_set.count():
				event_list += [1]
				for answer in post.post_set.all():
					add_post(answer)
				event_list += [-1]
		for post in self.post_set.all():
			add_post(post)
		return event_list
	
	def was_seen_by(self, user):
		return user in self.seen_by.all()
	
	def set_seen_by(self, user):
		self.seen_by.add(user)

	def set_last_post(self, new_last_post):
		self.seen_by.clear()
		self.last_post = new_last_post
		self.save()
	
	def __str__(self):
		if self.last_post is None:
			return "Thread: (empty)"
		return "Thread: {:.30} ~{}".format(self.last_post.content, self.last_post.user)

