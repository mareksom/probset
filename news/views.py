from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

from news.models import News
from django.utils import timezone
from utils.messages import error_msg, success_msg
from utils.pages import compute_pages

@login_required
def edit(request, ID):
	try:
		news = News.objects.get(id = ID)
	except News.DoesNotExist:
		error_msg(request, "Message with id={} does not exist.".format(ID))
		return redirect('news-news')

	if news.user != request.user:
		error_msg(request, "You don't have permissions to edit this message.")
		return redirect('news-news')

	context = {}

	if request.method == 'POST':
		if request.POST.get('remove', 'no-remove') != 'no-remove':
			news.delete()
			success_msg(request, "Message deleted successfully.")
			return redirect('news-news')

		news.title = request.POST.get('title','')
		news.text = request.POST.get('text','')

		try:
			if request.POST.get('preview', 'no-preview') != 'no-preview':
				news.check()
				context['preview'] = True

			else:
				news.save()
				success_msg(request, "Message edited successfully.")
				return redirect('news-news')

		except news.Error as error:
			error_msg(request, "Could not edit the message because of some errors.")
			context['error']  = error
	
	context['news'] = news

	return render(request, 'news/edit.html', context)

@login_required
def news(request, page=1):
	page = int(page)
	per_page = 10
	count_news = News.objects.count()
	context = compute_pages(page, count_news, 10)
	context['latest_news_list'] = News.objects.order_by('-created_date')[(page-1)*per_page : page*per_page]
	return render(request, 'news/news.html', context)

@login_required
def add(request):
	news = News()
	context = {}

	if request.method == 'POST':
		news.title = request.POST.get('title','')
		news.text = request.POST.get('text','')
		news.user = request.user

		try:
			if request.POST.get('preview', 'no-preview') != 'no-preview':
				news.check()
				context['preview'] = True

			else:
				news.save()
				success_msg(request, "Message created successfully.")
				return redirect('news-news')

		except news.Error as error:
			error_msg(request, "Could not create the message because of some errors.")
			context['error'] = error
	
	context['news'] = news

	return render(request,'news/add.html', context)
