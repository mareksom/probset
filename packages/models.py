from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from problems.models import Problem

import os

class Package(models.Model):

	def get_file_name(self, filename):
		return '/'.join(['packages', str(self.problem.id), timezone.now().strftime("%Y%m%d%H%M%S"), filename])

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	comment = models.TextField()
	problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
	package = models.FileField(upload_to=get_file_name)

	def delete(self):
		path, f = os.path.split(self.package.url[1:])
		os.remove(os.path.join(path, f))
		os.removedirs(path)
		super(Package, self).delete()

	def __str__(self):
		return "{} wrote {:.10}".format(self.user, self.comment)
