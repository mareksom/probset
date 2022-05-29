from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from django.core.exceptions import PermissionDenied

from packages.models import Package
from problems.models import Problem
from tags.models import Tag
from contests.models import Round

from utils.messages import error_msg, success_msg
from utils.pages import compute_pages
from utils.sort import pl_filter

from django.http import HttpResponse
import os
from django.conf import settings

from kasia.kasia import am_kasia, kasia_problem

import string

import re

import datetime

# decorator which handles non-existing problems
def get_problem(original_function):
	def new_function(request, **kwargs):
		try:
			kwargs['problem'] = Problem.objects.get(id = kwargs['problem'])
		except Problem.DoesNotExist:
			error_msg(request, "Problem with id={} does not exist.".format(kwargs['problem']))
			raise Http404
		return original_function(request, **kwargs)
	return new_function

# decorator which hendles non-existing packages and which checks if package belongs to a problem
def get_package(original_function):
	def new_function(request, **kwargs):
		try:
			kwargs['package'] = Package.objects.get(id = kwargs['package'])
		except Package.DoesNotExist:
			error_msg(request, "Package with id={} does not exist.".format(kwargs['package']))
			raise Http404
		if kwargs['package'].problem != kwargs['problem']:
			error_msg(request, "Package with id={} does not belong to this problem.".format(kwargs['package']))
			raise Http404
		return original_function(request, **kwargs)
	return new_function


@login_required
@get_problem
@kasia_problem
def solution(request, problem):
	context = {}

	context['problem'] = problem
	context['tab'] = 'solution'
	
	return render(request, 'problems/problem/solution.html', context)


@login_required
@get_problem
@kasia_problem
def contests(request, problem):

	context = {}

	context['problem'] = problem
	context['tab'] = 'contests'

	return render(request, 'problems/problem/contests.html', context)


@login_required
@get_problem
@kasia_problem
@get_package
def remove_package(request, problem, package):
	if package.user != request.user:
		error_msg(request, "You don't have permissions to remove this package.")
		raise PermissionDenied

	package.delete()
	success_msg(request, "Package was successfully deleted.")

	return redirect('problems-problem-packages', problem.id)


@login_required
@get_problem
@kasia_problem
@get_package
def download(request, problem, package):
	file_name = os.path.join(settings.BASE_DIR, package.package.url[1:])
	file_to_send = open(file_name, 'rb')
	response = HttpResponse(file_to_send.read(), content_type='application/x-compressed')
	file_to_send.close()

	response['Content-Disposition'] = 'attachment; filename={}'.format(os.path.split(package.package.url)[-1])

	return response


@login_required
@get_problem
@kasia_problem
def upload(request, problem):
	package = Package()
	context = {}

	if request.method == 'POST':
		package.user = request.user
		package.comment = request.POST.get('comment', '')
		package.problem = problem

		if re.search(r'^[a-zA-Z0-9_\.\-]+$', request.FILES['input_file'].name) is None:
			error_msg(request, "The file name may contain only those characters: {}{}_.-".format(string.ascii_letters, string.digits))
		else:
			package.package.save(request.FILES['input_file'].name, request.FILES['input_file'])
			package.save()
			success_msg(request, "Package uploaded successfully.")
			return redirect('problems-problem-packages', problem.id)

	context['problem'] = problem
	context['package'] = package
	context['tab'] = 'packages'

	return render(request, 'problems/problem/packages/upload.html', context)


@login_required
@get_problem
@kasia_problem
def packages(request, problem):
	packages = problem.package_set.order_by('-date').all()

	context = {}
	context['problem'] = problem
	context['packages'] = packages
	context['tab'] = 'packages'
	return render(request, 'problems/problem/packages/packages.html', context)


@login_required
@get_problem
@kasia_problem
def info(request, problem):
	context = {}
	context['problem'] = problem
	context['tab'] = 'info'
	return render(request, 'problems/problem/info.html', context)


@login_required
@get_problem
@kasia_problem
def comments(request, problem):
	context = {}
	context['thread'] = problem.comments
	context['problem'] = problem
	context['tab'] = 'comments'
	if am_kasia(request):
		if problem.user == request.user:
			problem.comments.set_seen_by(request.user)
	else:
		problem.comments.set_seen_by(request.user)
	return render(request, 'problems/problem/comments.html', context)


@login_required
def new(request):
	problem = Problem()
	
	context = {}

	if request.method == "POST":
		problem.title = request.POST.get('title','')
		problem.author = request.POST.get('author','')
		problem.description = request.POST.get('description','')
		problem.task = request.POST.get('task', '')
		problem.solution = request.POST.get('solution', '')
		problem.user = request.user
		try: problem.difficulty = int(request.POST.get('difficulty', '0'))
		except ValueError: problem.difficulty = 0
		try: problem.coolness = int(request.POST.get('coolness', '0'))
		except ValueError: problem.coolness = 0

		try:
			problem.save()

			for tag_id in request.POST.getlist('tags'):
				try:
					tag_obj = Tag.objects.get(id = tag_id)
					problem.tags.add(tag_obj)
				except tag.DoesNotExist: pass

			success_msg(request, "The problem was created successfully.")
			return redirect('problems-problem', problem.id)

		except problem.Error as error:
			error_msg(request, "Could not create the problem because of some errors.")
			context['error'] = error
	
	context['problem'] = problem

	tags = list(Tag.objects.all())
	tags.sort(key = lambda x : pl_filter(x.name.lower()))

	context['tags'] = tags

	selected_tags = []
	for tag_id in request.POST.getlist('tags'):
		try: selected_tags.append(int(tag_id))
		except ValueError: pass
	context['selected_tags'] = selected_tags

	return render(request, 'problems/new.html', context)


@login_required
@get_problem
@kasia_problem
def edit(request, problem):

	if request.user != problem.user:
		error_msg(request, "You don't have permissions to edit the problem with id={}".format(problem.id))
		raise PermissionDenied

	context = {'problem' : problem, 'tab' : 'edit'}

	tags = list(Tag.objects.all())
	tags.sort(key = lambda x : pl_filter(x.name.lower()))
	context['tags'] = tags
	
	if request.method == 'POST':
		if request.POST.get('remove','no-remove') != 'no-remove':
			problem.delete()
			success_msg(request, "Problem was deleted successfully.")
			return redirect('problems-problems')

		problem.title = request.POST.get('title','')
		problem.author = request.POST.get('author','')
		problem.description = request.POST.get('description','')
		problem.task = request.POST.get('task', '')
		problem.solution = request.POST.get('solution', '')

		try: problem.difficulty = int(request.POST.get('difficulty','0'))
		except ValueError: problem.difficulty = 0
		try: problem.coolness = int(request.POST.get('coolness','0'))
		except ValueError: problem.coolness = 0

		problem.tags.clear()
		for tag_id in request.POST.getlist('tags'):
			try:
				tag_obj = Tag.objects.get(id=int(tag_id))
				problem.tags.add(tag_obj)
			except ValueError: pass
			except Tag.DoesNotExist: pass

		try:
			problem.save()
			success_msg(request, "The problem was edited successfully.")

		except problem.Error as error:
			error_msg(request, "Couldn't edit the problem because of some errors.")
			context['error'] = error

	return render(request, 'problems/problem/edit.html', context)


@login_required
@get_problem
@kasia_problem
def task(request, problem):
	context = {'problem' : problem, 'tab' : 'task'}
	return render(request, 'problems/problem/task.html', context)


@login_required
@get_problem
@kasia_problem
def problem(request, problem):
	return redirect('problems-problem-info', problem.id)


@login_required
def problems(request):
	#log = open('/home/others/probset/probset/profiling.log', 'a')
	#log.write('[%s] poczatek\n' % (datetime.datetime.now()))
	if am_kasia(request):
		problems = Problem.objects.filter(user=request.user).order_by('-created_date')
	else:
		problems = Problem.objects.order_by('-created_date')
	context = {}
	if request.method == 'GET':
		context['search'] = {}
		search_title = request.GET.get('search_title', '')
		if search_title:
			context['search']['title'] = search_title
			problems = problems.filter(title__icontains = search_title)

		# difficulty
		context['difficulty'] = []
		tmp_query = Q()
		for difficulty in request.GET.getlist('difficulty'):
			try:
				tmp_query = tmp_query | Q(difficulty = int(difficulty))
				context['difficulty'].append(int(difficulty))
			except ValueError: pass
		problems = problems.filter(tmp_query)

		# coolness
		context['coolness'] = []
		tmp_query = Q()
		for coolness in request.GET.getlist('coolness'):
			try:
				tmp_query = tmp_query | Q(coolness = int(coolness))
				context['coolness'].append(int(coolness))
			except ValueError: pass
		problems = problems.filter(tmp_query)

		# tags
		context['selected_tags'] = []
		tmp_query = Q()
		for tag in request.GET.getlist('tags'):
			try:
				tag_object = Tag.objects.get(id = int(tag))
				tmp_query = tmp_query | Q(tags__id = int(tag))
				context['selected_tags'].append(int(tag))
			except ValueError: pass
		problems = problems.filter(tmp_query)

		# last_used
		last_used = request.GET.get('last_used', None)
		try:
			context['last_used'] = datetime.datetime.strptime(str(last_used), "%d-%m-%Y")

			# exclude problems with assigned contests ending after date 'last_used'
			problems = problems.prefetch_related('round_set__contest').exclude(
				round__contest__end_date__gt=context['last_used']).order_by('-created_date')
		except ValueError:
			context['last_used'] = None

		# my_problems
		tmp_query = Q()
		try:
			context['my_problems'] = request.GET.get('my_problems')
			if context['my_problems']:
				tmp_query |= Q(user=request.user.id)
		except ValueError:
			context['my_problems'] = None
		problems = problems.filter(tmp_query)

		# show all problems
		context['show_all'] = request.GET.get('show_all', 'False')

	context['tags'] = list(Tag.objects.all())
	context['tags'].sort(key = lambda x : pl_filter(x.name.lower()))

	#log.write('[%s] przed context[problems]\n' % (datetime.datetime.now()))
	context['problems'] = list(((problem, problem.comments.was_seen_by(request.user)) for problem in problems.all()))
	context['problems_count'] = len(context['problems'])

	#log.write('[%s] po context[problems]\n' % (datetime.datetime.now()))
	ret_val = render(request, 'problems/problems.html', context)
	#log.write('[%s] koniec\n' % (datetime.datetime.now()))
	#log.close()
	return ret_val
