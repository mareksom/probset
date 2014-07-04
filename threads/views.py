from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from threads.models import Post, Thread
from django.utils import timezone
from utils.messages import error_msg, success_msg

# decorator which handles non-existsing Posts
def get_post(original_function):
	def new_function(request, **kwargs):
		try:
			kwargs['post'] = Post.objects.get(id = kwargs['post'])
		except Post.DoesNotExist:
			error_msg(request, "Post with id={} does not exist.".format(kwargs['post']))
			raise Http404
		return original_function(request, **kwargs)
	return new_function

# decorator which handles non-existsing Threads
def get_thread(original_function):
	def new_function(request, **kwargs):
		try:
			kwargs['thread'] = Thread.objects.get(id = kwargs['thread'])
		except Thread.DoesNotExist:
			error_msg(request, "Thread with id={} does not exist.".format(kwargs['thread']))
			return Http404
		return original_function(request, **kwargs)
	return new_function

# decorator which authenticates the user (the post is accessible only to its owner)
def auth_post(original_function):
	def new_function(request, **kwargs):
		if request.user != kwargs.get('post', Post()).user:
			error_msg(request, "You don't have permissions to edit this post.")
			raise PermissionDenied
		return original_function(request, **kwargs)
	return new_function


@login_required
@get_post
@auth_post
def edit(request, post):
	context = {}

	if request.method == 'GET':
		context['next'] = request.GET.get('next', '')

	if request.method == 'POST':
		post.content = request.POST.get('post', '')
		context['next'] = request.POST.get('next', '')

		try:
			if request.POST.get('preview', 'no-preview') != 'no-preview':
				post.check()
				context['preview'] = True

			else:
				post.save()
				return redirect('{}#post-{}'.format(context['next'], post.id))

		except post.Error as error:
			error_msg(request, "Could not edit the post, because of some errors.")
			context['error'] = error

	context['post'] = post

	return render(request, 'threads/edit.html', context)


@login_required
@get_post
def reply(request, post):
	context = {}

	new_post = Post()

	new_post.answer_to = post
	new_post.user = request.user

	if request.method == 'GET':
		context['next'] = request.GET.get('next', '')

	if request.method == 'POST':
		new_post.content = request.POST.get('post', '')
		context['next'] = request.POST.get('next', '')

		try:
			if request.POST.get('preview', 'no-preview') != 'no-preview':
				new_post.check()
				context['preview'] = True

			else:
				new_post.save()
				return redirect('{}#post-{}'.format(context['next'], new_post.id))

		except new_post.Error as error:
			error_msg(request, "Could not create the post, because of some errros.")
			context['error'] = error

	context['post'] = post
	context['new_post'] = new_post
	return render(request, 'threads/reply.html', context)

@login_required
@get_thread
def new(request, thread):
	context = {}

	new_post = Post()

	new_post.thread = thread
	new_post.user = request.user

	if request.method == 'GET':
		context['next'] = request.GET.get('next', '')

	if request.method == 'POST':
		new_post.content = request.POST.get('post', '')
		context['next'] = request.POST.get('next', '')

		try:
			if request.POST.get('preview', 'no-preview') != 'no-preview':
				new_post.check()
				context['preview'] = True

			else:
				new_post.save()
				return redirect('{}#post-{}'.format(context['next'], new_post.id))

		except new_post.Error as error:
			error_msg(request, "Could not create the post, because of some errros.")
			context['error'] = error

	context['thread'] = thread
	context['new_post'] = new_post
	return render(request, 'threads/new.html', context)
