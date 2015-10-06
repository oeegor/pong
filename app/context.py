# coding: utf-8

from django.conf import settings
from django.core.urlresolvers import reverse

from social.backends.utils import load_backends


def build_context(request):
    urls = {
        'item_list': reverse('item_list'),
        'delete_item': reverse('delete_item'),
        'login_page': reverse('login'),
        'logout': reverse('logout'),
        'save_item': reverse('save_item'),
        'undo_delete_item': reverse('undo_delete_item'),
        'update_item': reverse('update_item'),
        'user_status': reverse('user_status'),
    }
    return {'ctx': {
        'auth_backends': load_backends(settings.AUTHENTICATION_BACKENDS).keys(),
        'urls': urls,
        'DEBUG': settings.DEBUG,
        'MEDIA_HASH': settings.MEDIA_HASH,
    }}
