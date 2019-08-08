from django.conf.urls import url
from impersonate.views import impersonate, stop_impersonate

urlpatterns = [
    url(r'^(?P<uid>\d+)/$', impersonate, name='impersonate-start'),
    url(r'^stop/$', stop_impersonate, name='impersonate-stop'),
]
