from django.conf.urls import patterns, url

from contests import views

urlpatterns = patterns('',
	url(r'^(?P<contest>[0-9]+)/round/(?P<round>[0-9]+)/attach/(?P<problem>[0-9]+)/$', 'contests.views.attach_problem', name='contests-contest-round-attach-problem'),
	url(r'^(?P<contest>[0-9]+)/round/(?P<round>[0-9]+)/detach/(?P<problem>[0-9]+)/$', 'contests.views.detach_problem', name='contests-contest-round-detach-problem'),
	url(r'^(?P<contest>[0-9]+)/round/(?P<round>[0-9]+)/attach/$', 'contests.views.attach', name='contests-contest-round-attach'),
	url(r'^(?P<contest>[0-9]+)/round/(?P<round>[0-9]+)/edit/$', 'contests.views.round_edit', name='contests-contest-round-edit'),
	url(r'^(?P<contest>[0-9]+)/round/add/$', 'contests.views.round_add', name='contests-contest-round-add'),
	url(r'^(?P<contest>[0-9]+)/edit/$', 'contests.views.edit', name='contests-contest-edit'),
	url(r'^(?P<contest>[0-9]+)/$', 'contests.views.contest', name='contests-contest'),
	url(r'^add/$', 'contests.views.add', name='contests-add'),
	url(r'^$', 'contests.views.contests', name='contests-contests'),
)
