# coding: utf-8

from django.conf import settings
from django.contrib.auth import logout as _logout
from django.http import HttpResponse
from django.shortcuts import redirect

from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.backends.google import GooglePlusAuth
from social.backends.utils import load_backends
from social..django_utils import psa

from utils import render_to


@render_to('login.html')
def login(request):
    if request.user.is_authenticated():
        return redirect('home')
    ctx = context()
    # ctx = build_context(request)
    # ctx['ctx_json'] = mark_safe(ujson.dumps(ctx['ctx']))
    return ctx


def logout(request):
    _logout(request)
    return redirect('home')


def context(**extra):
    return dict({
        'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
        'plus_scope': ' '.join(GooglePlusAuth.DEFAULT_SCOPE),
        'available_backends': load_backends(settings.AUTHENTICATION_BACKENDS)
    }, **extra)


@psa('social:complete')
def ajax_auth(request, backend):
    if isinstance(request.backend, BaseOAuth1):
        token = {
            'oauth_token': request.REQUEST.get('access_token'),
            'oauth_token_secret': request.REQUEST.get('access_token_secret'),
        }
    elif isinstance(request.backend, BaseOAuth2):
        token = request.REQUEST.get('access_token')
    else:
        raise Exception('Wrong backend type')
    user = request.backend.do_auth(token, ajax=True)
    login(request, user)
    return HttpResponse('ok')
