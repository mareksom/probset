from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'probset.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

		url(r'^$', 'news.views.news'),
		url(r'^accounts/', include('accounts.urls'), name='accounts'),
		url(r'^news/', include('news.urls'), name='news'),
		url(r'^help/', include('help.urls'), name='help'),
		url(r'^tags/', include('tags.urls'), name='tags'),
		url(r'^problems/', include('problems.urls'), name='problems'),
		url(r'^contests/', include('contests.urls'), name='contests'),

    url(r'^admin/', include(admin.site.urls)),
)
