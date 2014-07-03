from problems.models import Problem

def count_new_comments(user):
	return Problem.objects.count() - user.thread_set.filter(type='comment').count()
