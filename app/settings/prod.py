# coding: utf-8

import os

import dj_database_url

from common import *

DATABASES = {'default': dj_database_url.parse(os.environ['APP_DB'])}
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ['SOCIAL_AUTH_GOOGLE_OAUTH2_KEY']
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ['SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET']

_media_hash_path = os.path.join(os.environ['APP_ROOT'], '.media-hash')
MEDIA_HASH = open(_media_hash_path).read()

try:
    from .local import *
except ImportError:
    pass
