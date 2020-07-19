from django.conf.urls import include, url

import news.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'probset.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

		url(r'^$', news.views.news),
		url(r'^accounts/', include('accounts.urls'), name='accounts'),
		url(r'^news/', include('news.urls'), name='news'),
		url(r'^help/', include('help.urls'), name='help'),
		url(r'^tags/', include('tags.urls'), name='tags'),
		url(r'^problems/', include('problems.urls'), name='problems'),
		url(r'^contests/', include('contests.urls'), name='contests'),
		url(r'^threads/', include('threads.urls'), name='threads'),
		url(r'^forum/', include('forum.urls'), name='forum'),

		url(r'^su/', include('impersonate.urls'), name='impersonate'),
		url(r'^admin/', admin.site.urls),
]
