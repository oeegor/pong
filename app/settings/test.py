# coding: utf-8

from .common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pong',
        'USER': 'pong',
        'PASSWORD': 'pong',
        'HOST': 'localhost',
        'PORT': 5432,
        'TEST': {
            'NAME': 'test_pong',
        },
    },
}


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

try:
    from .local import *
except ImportError:
    pass
