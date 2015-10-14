# coding: utf-8

import os

import dj_database_url

from common import *

DATABASES = {'default': dj_database_url.parse(os.environ['APP_DB'])}

RAVEN_CONFIG = {
    'dsn': os.environ['SENTRY_DSN'],
}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ['SOCIAL_AUTH_GOOGLE_OAUTH2_KEY']
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ['SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET']

EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

try:
    from .local import *
except ImportError:
    pass
