# coding: utf-8

from .common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pong',
        'USER': 'postgres',
        'PASSWORD': '2minutes2midnight',
        'HOST': 'dev94-db.ostrovok.ru',
        'PORT': 5432,
        'TEST': {
            'NAME': 'test_pong',
        },
    },
}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '825542354894-9qevqrfg2d7ps5ndhod49770b1rr19ul.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'EPOiiNGWFGZjJBstu3MOARDl'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    from .local import *
except ImportError:
    pass
