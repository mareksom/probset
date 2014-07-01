from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

from forum.models import Post, Thread
from django.utils import timezone
from utils.messages import error_msg, success_msg
from utils.pages import compute_pages

# decorator which handles non-existsing threads
def get_thread(original_function):
	def new_function(request, **kwargs):
		try:
			kwargs['thread'] = Thread.objects.get(id = kwargs['thread'])
		except Thread.DoesNotExist:
			error_msg(request, "Thread with id={} does not exist.".format(kwargs['thread']))
			return redirect('forum-threads')
		return original_function(request, **kwargs)
	return new_function

# decorator which handles non-existsing Posts
def get_post(original_function):
	def new_function(request, **kwargs):
		try:
			kwargs['post'] = Post.objects.get(id = kwargs['post'])
		except Post.DoesNotExist:
			error_msg(request, "Post with id={} does not exist.".format(kwargs['post']))
			return redirect('forum-threads')
		return original_function(request, **kwargs)
	return new_function

# decorator which authenticates the user (the post is accessible only to its owner)
def auth_post(original_function):
	def new_function(request, **kwargs):
		if request.user != kwargs.get('post', Post()).user:
			error_msg(request, "You don't have permissions to edit this post.")
			return redirect('forum-threads')
		return original_function(request, **kwargs)
	return new_function


@login_required
def new_thread(request):
	context = {}

	thread = Thread()
	post = Post()
	post.user = request.user

	if request.method == 'POST':
		thread.title = request.POST.get('title', '')
		post.content = request.POST.get('post', '')

		try:
			if request.POST.get('preview', 'no-preview') != 'no-preview':
				thread.check()
				post.check()
				context['preview'] = True

			else:
				thread.check()
				post.save()
				thread.save()
				post.thread = thread
				post.save()
				post.update_last_post()
				success_msg(request, "Thread created successfully.")
				return redirect('forum-thread', thread.id)

		except (thread.Error, post.Error) as error:
			error_msg(request, "Could not create the thread because of some errors.")
			context['error'] = error
	
	context['thread'] = thread
	context['post'] = post

	return render(request, 'forum/new_thread.html', context)


@login_required
@get_post
@auth_post
def edit(request, post):
	context = {}

	if request.method == 'POST':
		post.content = request.POST.get('post', '')

		try:
			if request.POST.get('preview', 'no-preview') != 'no-preview':
				post.check()
				context['preview'] = True

			else:
				post.save()
				return redirect('forum-thread', post.get_thread().id)

		except post.Error as error:
			error_msg(request, "Could not edit the post, because of some errors.")
			context['error'] = error

	context['post'] = post

	return render(request, 'forum/edit.html', context)


@login_required
@get_post
def reply(request, post):
	context = {}

	new_post = Post()

	new_post.answer_to = post
	new_post.user = request.user

	if request.method == 'POST':
		new_post.content = request.POST.get('post', '')

		try:
			if request.POST.get('preview', 'no-preview') != 'no-preview':
				new_post.check()
				context['preview'] = True

			else:
				new_post.save()
				return redirect('forum-thread', new_post.get_thread().id)

		except new_post.Error as error:
			error_msg(request, "Could not create the post, because of some errros.")
			context['error'] = error

	context['post'] = post
	context['new_post'] = new_post
	return render(request, 'forum/reply.html', context)


@login_required
@get_thread
def thread(request, thread):
	context = {}
	posts = []

	def add_post(post):
		nonlocal posts
		posts += [post]
		if post.post_set.count():
			posts += [1]
			for answer in post.post_set.all():
				add_post(answer)
			posts += [-1]

	for post in thread.post_set.all():
		add_post(post)

	context['thread'] = thread
	context['posts'] = posts
	return render(request, 'forum/thread.html', context)


@login_required
def threads(request, page=1):
	page = int(page)
	per_page = 20
	count_threads = Thread.objects.count()
	context = compute_pages(page, count_threads, per_page)
	context['threads'] = Thread.objects.order_by('-created_date')[(page - 1) * per_page : page * per_page]
	return render(request, 'forum/threads.html', context)
