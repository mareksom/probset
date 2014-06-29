import os, sys

sys.path.append('/home/mareksom/www/probset')
sys.path.append('/home/mareksom/www/probset/probset')

os.environ['DJANGO_SETTINGS_MODULE'] = 'probset.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
