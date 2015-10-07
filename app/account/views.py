# coding: utf-8

from django.contrib.auth import logout as _logout
from django.http import HttpResponse
from django.shortcuts import redirect


def login(request):
    if request.user.is_authenticated():
        return redirect('home')
    return redirect('social:begin', backend='google-oauth2')


def logout(request):
    _logout(request)
    if 'noredirect' in request.GET:
        return HttpResponse('done')
    return redirect('home')
