from django.conf.urls import patterns, url


urlpatterns = patterns('impersonate.views',
    url(r'^(?P<uid>\d+)/$', 'impersonate', name='impersonate-start'),
    url(r'^stop/$', 'stop_impersonate', name='impersonate-stop'),
)
