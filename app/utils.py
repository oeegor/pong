# coding: utf-8

from functools import wraps

from django.shortcuts import render


def render_to(tpl):
    def decorator(func):
        @wraps(func)
        def wrr(request, *args, **kwargs):
            out = func(request, *args, **kwargs)
            if isinstance(out, dict):
                out = render(request, tpl, out)
            return out
        return wrr
    return decorator
