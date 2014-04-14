from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader

def home(request):
	return render(request, 'menu.html', {})
