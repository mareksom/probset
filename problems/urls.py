from django.conf.urls import patterns, url

from problems import views

urlpatterns = patterns('',
	url(r'^(?P<ID>[0-9]+)/packages/upload/$', views.upload, name='problems-problem-packages-upload'),
	url(r'^(?P<ID>[0-9]+)/packages/(?P<packageID>[0-9]+)/remove/$', views.remove_package, name='problems-problem-packages-remove'),
	url(r'^(?P<ID>[0-9]+)/packages/(?P<packageID>[0-9]+)/download/$', views.download, name='problems-problem-packages-download'),
	url(r'^(?P<ID>[0-9]+)/packages/$', views.packages, name='problems-problem-packages'),
	url(r'^(?P<ID>[0-9]+)/info/$', views.info, name='problems-problem-info'),

	url(r'^(?P<ID>[0-9]+)/comments/edit/(?P<comID>[0-9]+)/$', views.comments_edit, name='problems-problem-comments-edit'),
	url(r'^(?P<ID>[0-9]+)/comments/add/$', views.comments_add, name='problems-problem-comments-add'),
	url(r'^(?P<ID>[0-9]+)/comments/(?P<page>[0-9]+)/$', views.comments, name='problems-problem-comments'),
	url(r'^(?P<ID>[0-9]+)/comments/$', views.comments, name='problems-problem-comments'),

	url(r'^(?P<ID>[0-9]+)/task/$', views.task, name='problems-problem-task'),
	url(r'^(?P<ID>[0-9]+)/edit/$', views.edit, name='problems-problem-edit'),
	url(r'^(?P<ID>[0-9]+)/$', views.problem, name='problems-problem'),
	url(r'^new/$', views.new, name='problems-new'),
	url(r'^$', views.problems, name='problems-problems'),
)
