from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^packages/upload/$', 'problems.views.upload', name='problems-problem-packages-upload'),
	url(r'^packages/(?P<package>[0-9]+)/remove/$', 'problems.views.remove_package', name='problems-problem-packages-remove'),
	url(r'^packages/(?P<package>[0-9]+)/download/$', 'problems.views.download', name='problems-problem-packages-download'),
	url(r'^packages/$', 'problems.views.packages', name='problems-problem-packages'),
	url(r'^info/$', 'problems.views.info', name='problems-problem-info'),

	url(r'^comments/edit/(?P<comment>[0-9]+)/$', 'problems.views.comments_edit', name='problems-problem-comments-edit'),
	url(r'^comments/add/$', 'problems.views.comments_add', name='problems-problem-comments-add'),
	url(r'^comments/(?P<page>[0-9]+)/$', 'problems.views.comments', name='problems-problem-comments'),
	url(r'^comments/$', 'problems.views.comments', name='problems-problem-comments'),

	url(r'^contests/$', 'problems.views.contests', name='problems-problem-contests'),

	url(r'^task/$', 'problems.views.task', name='problems-problem-task'),
	url(r'^edit/$', 'problems.views.edit', name='problems-problem-edit'),
	url(r'^$', 'problems.views.problem', name='problems-problem'),
)
