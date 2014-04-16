from django.conf.urls import patterns, url

from tags import views

urlpatterns = patterns('',
	url(r'^add/$', views.add, name='tags-add'),
	url(r'^(?P<ID>[0-9]+)/$', views.edit, name='tags-edit'),
	url(r'^$', views.index, name='tags-tags'),
)
