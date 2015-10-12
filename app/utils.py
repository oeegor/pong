# coding: utf-8

from functools import wraps

from django.shortcuts import render


def render_to(tpl):
    def decorator(func):
        @wraps(func)
        def wrr(request, *args, **kwargs):
            result = func(request, *args, **kwargs)
            if isinstance(result, dict):
                result['quote'] = get_random_quote()
                rendered = render(request, tpl, result)
            else:
                rendered = result
            return rendered
        return wrr
    return decorator


def get_random_quote():
    from core.models import Quote
    return Quote.objects.all().order_by('?').first()
