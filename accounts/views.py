from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as sup_logout
from django.contrib.auth import login as sup_login
from django.contrib.auth import  authenticate

from django.contrib.auth.models import User

from utils.messages import error_msg, success_msg

@login_required
def settings(request):
	user = request.user
	context = {'first_name' : user.first_name, 'last_name' : user.last_name}
	if request.method == 'POST':
		context['first_name'] = request.POST.get('first','')
		context['last_name']  = request.POST.get('last', '')

		if context['first_name'] == '':
			error_msg(request, "First name cannot be empty.")

		elif context['last_name'] == '':
			error_msg(request, "Last name cannot be empty.")

		elif not user.check_password(request.POST.get('oldpassword','')):
			error_msg(request, "Password not correct.")

		elif request.POST.get('newpassword','') != request.POST.get('repeatpassword',''):
			error_msg(request, "New passwords differ.")

		else:
			if request.POST.get('newpassword','') != '':
				user.set_password(request.POST['newpassword'])
			user.first_name = context['first_name']
			user.last_name = context['last_name']
			user.save()
			success_msg(request, "Your new settings was saved.")
			return redirect('accounts-settings')

	return render(request, 'accounts/settings.html', context)

@login_required
def users(request):
	users = User.objects.all()
	context = {'users': users}
	return render(request, 'accounts/users.html', context)

@login_required
def user(request,ID):
	try:
		user = User.objects.get(id=ID)
	except User.DoesNotExist:
		error_msg(request, "User with id={} does not exist.".format(ID))
		raise Http404
	context = {'user': user}
	return render(request, 'accounts/user.html', context)

def login(request):
	if request.user.is_authenticated():
		return redirect('accounts-users')
	messages = []
	if request.method == 'POST':
		username = request.POST.get('username','')
		password = request.POST.get('password','')
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				sup_login(request, user)

				page_to_redirect = request.GET.get('next', '')
				if page_to_redirect:
					return redirect(page_to_redirect)
				return redirect('news-news')

			else:
				error_msg(request, 'Your account is disabled.')
		else:
			error_msg(request, 'Wrong username or password.')
	return render(request, 'accounts/login.html')

@login_required
def logout(request):
	sup_logout(request)
	return redirect('login')
