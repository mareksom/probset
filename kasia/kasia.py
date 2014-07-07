from problems.models import Problem
from contests.models import Contest
from django.shortcuts import render

KASIA_USERNAME = 'elvina'
KASIA_CONTESTS = (2, )

def am_kasia(request):
	return request.user.username == KASIA_USERNAME

def kasia_in_contest(contest):
	return contest.id in KASIA_CONTESTS

def not_kasia(original_function):
	def new_function(request, **kwargs):
		if am_kasia(request):
			return render(request, 'kasia/nope.html', {'not' : True})
		return original_function(request, **kwargs)
	return new_function

def kasia_problem(original_function):
	def new_function(request, **kwargs):
		if not am_kasia(request):
			return original_function(request, **kwargs)
		problem = kwargs.get('problem', Problem())
		if problem.user.username == KASIA_USERNAME:
			return original_function(request, **kwargs)
		for round in problem.round_set.all():
			if round.contest.id in KASIA_CONTESTS:
				return original_function(request, **kwargs)
		return render(request, 'kasia/nope.html', {'problem' : True})
	return new_function

def kasia_contest(original_function):
	def new_function(request, **kwargs):
		if not am_kasia(request):
			return original_function(request, **kwargs)
		contest = kwargs.get('contest', Contest())
		if contest.id in KASIA_CONTESTS:
			return original_function(request, **kwargs)
		return render(request, 'kasia/nope.html', {'contest' : True})
	return new_function

def kasia_own_problem(original_function):
	def new_function(request, **kwargs):
		if not am_kasia(request):
			return original_function(request, **kwargs)
		problem = kwargs.get('problem', Problem())
		if problem.user == request.user:
			return original_function(request, **kwargs)
		return render(request, 'kasia/nope.html', {'own_problem' : True})
	return new_function
