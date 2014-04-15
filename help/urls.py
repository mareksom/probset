from django.conf.urls import patterns, url

from help import views

urlpatterns = patterns('',
	url(r'^bbcode/$', views.bbcode, name='help-bbcode'),
	url(r'^difficulty/$', views.difficulty, name='help-difficulty'),
	url(r'^$', views.help, name='help-help'),
)
