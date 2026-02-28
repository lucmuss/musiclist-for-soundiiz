"""WSGI config for musiclist_project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "musiclist_project.settings")

application = get_wsgi_application()
