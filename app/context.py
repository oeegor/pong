# coding: utf-8

from django.conf import settings
from django.core.urlresolvers import reverse

from social_core.backends.utils import load_backends


def build_context(request):
    urls = {
        'login_page': reverse('login'),
        'logout': reverse('logout'),
    }
    return {'ctx': {
        'auth_backends': list(load_backends(settings.AUTHENTICATION_BACKENDS).keys()),
        'urls': urls,
        'DEBUG': settings.DEBUG,
        # 'MEDIA_HASH': settings.MEDIA_HASH,
    }}
