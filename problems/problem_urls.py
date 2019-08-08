from django.conf.urls import url
import problems.views

urlpatterns = [
	url(r'^packages/upload/$', problems.views.upload, name='problems-problem-packages-upload'),
	url(r'^packages/(?P<package>[0-9]+)/remove/$', problems.views.remove_package, name='problems-problem-packages-remove'),
	url(r'^packages/(?P<package>[0-9]+)/download/$', problems.views.download, name='problems-problem-packages-download'),
	url(r'^packages/$', problems.views.packages, name='problems-problem-packages'),
	url(r'^info/$', problems.views.info, name='problems-problem-info'),

	url(r'^comments/$', problems.views.comments, name='problems-problem-comments'),

	url(r'^contests/$', problems.views.contests, name='problems-problem-contests'),
	url(r'^solution/$', problems.views.solution, name='problems-problem-solution'),
	url(r'^task/$', problems.views.task, name='problems-problem-task'),
	url(r'^edit/$', problems.views.edit, name='problems-problem-edit'),
	url(r'^$', problems.views.problem, name='problems-problem'),
]
