from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q

from packages.models import Package
from problems.models import Problem
from comments.models import Comment
from tags.models import Tag

from utils.messages import error_msg, success_msg
from utils.pages import compute_pages
from utils.sort import pl_filter

from django.http import HttpResponse
import os
from django.conf import settings

import string

import re

@login_required
def remove_package(request, ID, packageID):
	try:
		problem = Problem.objects.get(id = ID)
	except Problem.DoesNotExist:
		error_msg(request, "Problem with id={} does not exist.".format(ID))
		return redirect('problems-problems')

	try:
		package = Package.objects.get(id = packageID)
	except Package.DoesNotExist:
		error_msg(request, "Package with id={} does not exist.".format(packageID))
		return redirect('problems-problem-packages', ID)
	
	if package.problem != problem:
		error_msg(request, "Package with id={} does not belong to the problem with id={}.".format(packageID, ID))
		return redirect('problems-problem-packages', ID)
	
	package.delete()
	success_msg(request, "Package was successfully deleted.")

	return redirect('problems-problem-packages', ID)

@login_required
def upload(request, ID):
	try:
		problem = Problem.objects.get(id = ID)
	except Problem.DoesNotExist:
		error_msg(request, "Problem with id={} does not exist.".format(ID))
		return redirect('problems-problems')
	
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
			return redirect('problems-problem-packages', ID)

	context['problem'] = problem
	context['package'] = package
	context['tab'] = 'packages'

	return render(request, 'problems/problem/packages/upload.html', context)

@login_required
def download(request, ID, packageID):
	try:
		problem = Problem.objects.get(id = ID)
	except Problem.DoesNotExist:
		error_msg(request, "Problem with id={} does not exist.".format(ID))
		return redirect('problems-problems')
	
	try:
		package = Package.objects.get(id = packageID)
	except Package.DoesNotExist:
		error_msg(request, "Package with id={} does not exist.".format(packageID))
		return redirect('problems-problem', ID)
	
	if package.problem != problem:
		error_msg(request, "Package with id={} does not belong to the problem with id={}.".format(packageID, ID))
		return redirect('problems-problem', ID)
	
	file_name = os.path.join(settings.BASE_DIR, package.package.url[1:])
	file_to_send = open(file_name, 'rb')
	response = HttpResponse(file_to_send.read(), content_type='application/x-compressed')
	file_to_send.close()

	response['Content-Disposition'] = 'attachment; filename={}'.format(os.path.split(package.package.url)[-1])

	return response

@login_required
def packages(request, ID):
	try:
		problem = Problem.objects.get(id = ID)
	except Problem.DoesNotExist:
		error_msg(request, "Problem with id={} does not exist.".format(ID))
		return redirect('problems-problems')

	packages = problem.package_set.order_by('-date').all()

	context = {}
	context['problem'] = problem
	context['packages'] = packages
	context['tab'] = 'packages'
	return render(request, 'problems/problem/packages/packages.html', context)

@login_required
def info(request, ID):
	try:
		problem = Problem.objects.get(id = ID)
	except Problem.DoesNotExist:
		error_msg(requesst, "Problem with id={} does not exist.".format(ID))
		return redirect('problems-problems')

	context = {}
	context['problem'] = problem
	context['tab'] = 'info'
	return render(request, 'problems/problem/info.html', context)

@login_required
def comments_edit(request, ID, comID):
	try:
		problem = Problem.objects.get(id = ID)
	except Problem.DoesNotExist:
		error_msg(request, "Problem with id={} does not exist.".format(ID))
		return redirect('problems-problems')
	
	try:
		comment = Comment.objects.get(id = comID)
	except Comment.DoesNotExist:
		error_msg(request, "Comment with id = {} does not exist.".format(comID))
		return redirect('problems-problem-comments', ID)
	
	if comment.problem != problem:
		error_msg(request, "Comment {} does not belong to problem {}.".format(comID, ID))
		return redirect('problems-problems')
	
	if comment.user != request.user:
		error_msg(request, "You don't have permissions to edit this comment.")
		return redirect('problems-problem-comments', ID)
	
	context = {'problem' : problem, 'tab': 'comments'}

	if request.method == "POST":
		comment.comment = request.POST.get('comment', '')
		comment.date = timezone.now()
		try:
			if request.POST.get('preview', 'no-preview') != 'no-preview':
				context['preview'] = True
				comment.check()

			elif request.POST.get('edit', 'no-edit') != 'no-edit':
				comment.save()
				success_msg(request, "Your comment was edited successfully.")
				return redirect('problems-problem-comments', ID)

			else:
				comment.delete()
				success_msg(request, "Your comment was successfully deleted.")
				return redirect('problems-problem-comments', ID)

		except comment.Error as error:
			error_msg(request, "There were some errors while editing your comments.")
			context['error'] = error
	
	context['comment'] = comment

	return render(request, 'problems/problem/comments/comments_edit.html', context)

@login_required
def comments_add(request, ID):
	try:
		problem = Problem.objects.get(id = ID)
	except Problem.DoesNotExist:
		error_msg(request, "Problem with id={} does not exist.".format(ID))
		return redirect('problems-problems')
	
	comment = Comment()
	comment.user = request.user

	context = {'problem' : problem, 'tab': 'comments'}

	if request.method == "POST":
		comment.comment = request.POST.get('comment', '')
		comment.problem = problem
		comment.date = timezone.now()
		try:
			if request.POST.get('preview', 'no-preview') != 'no-preview':
				context['preview'] = True
				comment.check()

			else:
				comment.save()
				success_msg(request, "Your comment was added successfully.")
				return redirect('problems-problem-comments', ID)

		except comment.Error as error:
			error_msg(request, "Could not create comment because of error.")
			context['error'] = error
	
	context['comment'] = comment

	return render(request, 'problems/problem/comments/comments_add.html', context)

@login_required
def comments(request, ID, page=1):
	page = int(page)
	per_page = 10

	try:
		problem = Problem.objects.get(id = ID)
	except Problem.DoesNotExist:
		error_msg(request, "Problem with id={} does not exist.".format(ID))
		return redirect('problems-problems')
	
	context = compute_pages(page, problem.comment_set.count(), per_page)

	context['problem'] = problem
	context['tab'] = 'comments'

	comments = problem.comment_set.order_by('-created_date')[(page-1)*per_page:page*per_page].all()

	context['comments'] = comments

	return render(request, 'problems/problem/comments/comments.html', context)

@login_required
def new(request):
	problem = Problem()
	
	context = {}

	if request.method == "POST":
		problem.title = request.POST.get('title','')
		problem.author = request.POST.get('author','')
		problem.description = request.POST.get('description','')
		problem.task = request.POST.get('task', '')
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
def edit(request, ID):
	try:
		problem = Problem.objects.get(id = ID)
	except Problem.DoesNotExist:
		error_msg(request, "Problem with id={} does not exist.".format(ID))
		return redirect('problems-problems')
	
	if request.user != problem.user:
		error_msg(request, "You don't have permissions to edit the problem with id={}".format(ID))
		return redirect('problems-problems')

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
def task(request, ID):
	try:
		problem = Problem.objects.get(id = ID)
	except Problem.DoesNotExist:
		error_msg(request, "Problem with id={} does not exist.".format(ID))
		return redirect('problems-problems')

	context = {'problem' : problem, 'tab' : 'task'}
	return render(request, 'problems/problem/task.html', context)

@login_required
def problem(request, ID):
	return redirect('problems-problem-info', ID)

@login_required
def problems(request):
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
	
	context['tags'] = list(Tag.objects.all())
	context['tags'].sort(key = lambda x : pl_filter(x.name.lower()))

	context['problems'] = problems.all()
	return render(request, 'problems/problems.html', context)
