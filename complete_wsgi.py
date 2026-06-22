"""
WSGI config for mini_hemis project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini_hemis.settings')

application = get_wsgi_application()
