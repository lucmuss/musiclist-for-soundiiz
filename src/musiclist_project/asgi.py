"""ASGI config for musiclist_project."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "musiclist_project.settings")

application = get_asgi_application()
