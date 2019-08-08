from problems.models import Problem
from kasia.kasia import am_kasia, KASIA_USERNAME

def count_new_comments(user):
	if user.username == KASIA_USERNAME:
		return Problem.objects.filter(user=user).count() - user.thread_set.filter(type='comment').count()
	return Problem.objects.count() - user.thread_set.filter(type='comment').count()
