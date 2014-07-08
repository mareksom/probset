from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from forum.models import ForumThread
from threads.models import Post
from django.utils import timezone
from utils.messages import error_msg, success_msg
from utils.pages import compute_pages

# decorator which handles non-existsing threads
def get_forumthread(original_function):
	def new_function(request, **kwargs):
		try:
			kwargs['thread'] = ForumThread.objects.get(id = kwargs['thread'])
		except ForumThread.DoesNotExist:
			error_msg(request, "Thread with id={} does not exist.".format(kwargs['thread']))
			raise Http404
		return original_function(request, **kwargs)
	return new_function


@login_required
def new_thread(request):
	context = {}

	thread = ForumThread()
	new_post = Post()

	if request.method == 'POST':
		thread.title = request.POST.get('title', '')
		new_post.content = request.POST.get('post', '')
		new_post.user = request.user

		try:
			if request.POST.get('preview', 'no-preview') != 'no-preview':
				thread.check()
				new_post.check()
				context['preview'] = True

			else:
				thread.check()
				new_post.check()
				thread.save()
				new_post.thread = thread.thread
				new_post.save()
				success_msg(request, "Thread created successfully.")
				return redirect('forum-thread', thread.id)

		except thread.Error as error:
			error_msg(request, "Could not create the thread because of some errors.")
			context['error'] = error

		except new_post.Error as error:
			error_msg(request, "Could not create the thread because of some errors.")
			context['error'] = error
	
	context['thread'] = thread
	context['new_post'] = new_post

	return render(request, 'forum/new_thread.html', context)



@login_required
@get_forumthread
def thread(request, thread):
	context = {}
	context['thread'] = thread
	thread.thread.set_seen_by(request.user)
	return render(request, 'forum/thread.html', context)


@login_required
def threads(request, page=1):
	page = int(page)
	per_page = 20
	count_threads = ForumThread.objects.count()
	context = compute_pages(page, count_threads, per_page)
	objects = ForumThread.objects.order_by('-thread__last_post__edited_date')[(page - 1) * per_page : page * per_page]
	context['threads'] = ((thread, thread.thread.was_seen_by(request.user)) for thread in objects)
	return render(request, 'forum/threads.html', context)
