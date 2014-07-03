from forum.models import ForumThread

def count_new_forum_threads(user):
	return ForumThread.objects.count() - user.thread_set.filter(type='forum').count()
