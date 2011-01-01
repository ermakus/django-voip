import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

BASEDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append( BASEDIR )

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

