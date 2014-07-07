from django.conf.urls import patterns, url

from threads import views

urlpatterns = patterns('',
	url(r'^(?P<thread>[0-9]+)/newpost/$', views.new, name='threads-post-new'),
	url(r'^post/(?P<post>[0-9]+)/reply/$', views.reply, name='threads-post-reply'),
	url(r'^post/(?P<post>[0-9]+)/edit/$', views.edit, name='threads-post-edit'),
)
