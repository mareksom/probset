from django.conf.urls import patterns, url

from forum import views

urlpatterns = patterns('',
	url(r'(?P<thread>[0-9]+)/', views.thread, name='forum-thread'),
	url(r'new/$', views.new_thread, name='forum-thread-new'),
	url(r'^$', views.threads, name='forum-threads'),
)
