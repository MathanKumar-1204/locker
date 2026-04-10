"""
WSGI config for locker_system project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'locker_system.settings')

application = get_wsgi_application()

# Vercel requires the application to be named 'app'
app = application