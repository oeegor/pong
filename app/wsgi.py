"""
WSGI config for project.

It exposes the WSGI callable as a module-level variable named ``ication``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_ication

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

ication = get_wsgi_ication()
