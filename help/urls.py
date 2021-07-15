from django.conf.urls import url

from help import views

urlpatterns = [
	url(r'^problems/$', views.problems, name='help-problems'),
	url(r'^bbcode/$', views.bbcode, name='help-bbcode'),
	url(r'^latex/$', views.latex, name='help-latex'),
	url(r'^difficulty/$', views.difficulty, name='help-difficulty'),
	url(r'^markdown/$', views.markdown, name='help-markdown'),
	url(r'^$', views.help, name='help-help'),
]
