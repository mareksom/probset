from django.conf.urls import include, url
import problems.views

urlpatterns = [
	url(r'^(?P<problem>[0-9]+)/', include('problems.problem_urls')),
	url(r'^new/$', problems.views.new, name='problems-new'),
	url(r'^$', problems.views.problems, name='problems-problems'),
]
