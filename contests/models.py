from django.db import models

from problems.models import Problem

import re
from datetime import date
import time

class Contest(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	begin_date = models.DateField()
	end_date = models.DateField()

	class Error(Exception):
		name = ''
		begin_date = ''
		end_date = ''
		def is_error(self):
			return self.name != '' or self.begin_date != '' or self.end_date != ''
	
	def check(self):
		err = self.Error()
		if not 0 < len(self.name) <= 100:
			err.name = "Contest name length should be from range [1, 100]."

		if type(self.begin_date) is str:
			try:
				self.begin_date = date.fromtimestamp(time.mktime(time.strptime(self.begin_date, "%d-%m-%Y")))
			except ValueError:
				err.begin_date = 'The date should be given in format "dd-mm-yyyy".'
		elif self.begin_date is None:
			err.begin_date = "You must specify the date of the beginning of the contest."

		if type(self.end_date) is str:
			try:
				self.end_date = date.fromtimestamp(time.mktime(time.strptime(self.end_date, "%d-%m-%Y")))
			except ValueError:
				err.end_date = 'The date should be given in format "dd-mm-yyyy".'
		elif self.end_date is None:
			err.end_date = "You must specify the date of the end of the contest."

		if not err.begin_date and not err.end_date:
			if self.begin_date > self.end_date:
				err.begin_date = "The contest cannot begin after the end of the contest."
				err.end_date = "The contest cannot end before the beginning of the contest."

		if err.is_error():
			raise err

	def save(self):
		self.check()
		super(Contest, self).save()

	def __str__(self):
		return self.name


class Round(models.Model):
	name = models.CharField(max_length=100)
	problems = models.ManyToManyField(Problem, blank=True)

	contest = models.ForeignKey(Contest)

	class Error(Exception):
		name = ''
		def is_error(self):
			return self.name != ''
	
	def check(self):
		err = self.Error()

		if not 0 < len(self.name) <= 100:
			err.name = "Round name length should be from range [1, 100]."

		if err.is_error():
			raise err

	def save(self):
		self.check()
		super(Round, self).save()

	def __str__(self):
		return self.name
