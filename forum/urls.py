from django.conf.urls import patterns, url

from forum import views

urlpatterns = patterns('',
	url(r'^thread/new$', views.new_thread, name='forum-thread-new'),
	url(r'^post/(?P<post>[0-9]+)/reply/$', views.reply, name='forum-post-reply'),
	url(r'^pos/(?P<post>[0-9]+)/edit/$', views.edit, name='forum-post-edit'),
	url(r'^thread/(?P<thread>[0-9]+)/$', views.thread, name='forum-thread'),
	url(r'^(?P<page>[0-9]+)/$', views.threads, name='forum-threads'),
	url(r'^$', views.threads, name='forum-threads'),
)
