from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from utils.messages import error_msg, success_msg

from tags.models import Tag

from utils.sort import pl_filter

@login_required
def edit(request, ID):
	try:
		tag = Tag.objects.get(id = ID)
	except tag.DoesNotExist:
		error_msg(request, "Tag with id = {} does not exist.".format(ID))
		return redirect('tags-tags')
	
	context = {}
	
	if request.method == 'POST':
		if request.POST.get('remove', 'no-remove') != 'no-remove':
			tag.delete()
			success_msg(request, "Tag was deleted successfully.")
			return redirect('tags-tags')

		tag.name = request.POST.get('name', '')
		tag.short = request.POST.get('short', '')
		tag.color = request.POST.get('color', '')

		try:
			tag.save()
			success_msg(request, "Tag was edited successfully.")
			return redirect('tags-tags')
		except tag.Error as error:
			error_msg(request, "Tag could not be edited because of some errors.")
			context['error'] = error
	
	context['tag'] = tag
	return render(request, 'tags/edit.html', context)

@login_required
def add(request):
	tag = Tag()
	tag.name = ''
	tag.short = ''
	tag.color = '#F0F0F0' # default color
	
	context = {}

	if request.method == 'POST':
		tag.name = request.POST.get('name', '')
		tag.short = request.POST.get('short', '')
		tag.color = request.POST.get('color', '')
		try:
			tag.save()
			success_msg(request, "Tag was added successfully.")
			return redirect('tags-tags')
		except tag.Error as error:
			error_msg(request, "Could not add the tag because of some errors.")
			context['error'] = error

	context['tag'] = tag
	return render(request, 'tags/add.html', context)

@login_required
def index(request):
	search = request.GET.get('search', '')
	tags = list(Tag.objects.filter(name__icontains=search).all())
	tags.sort(key = lambda x : pl_filter(x.name.lower()))
	context = {'tags' : tags, 'search' : search}
	return render(request, 'tags/tags.html', context)
