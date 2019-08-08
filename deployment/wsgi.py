import os, sys
"""
os.environ['DJANGO_SETTINGS_MODULE'] = 'probset.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
"""
from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'probset.settings'
application = get_wsgi_application()
