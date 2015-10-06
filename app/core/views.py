# coding: utf-8

from django.utils.html import mark_safe
import ujson

from context import build_context
from utils import render_to


@render_to('index.html')
def home(request):
    ctx = build_context(request)
    ctx['ctx_json'] = mark_safe(ujson.dumps(ctx['ctx']))
    return ctx
