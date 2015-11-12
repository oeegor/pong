# coding: utf-8

from django.contrib.auth.decorators import login_required

from rating.logic import get_rating_list
from utils import render_to


@login_required(login_url='/login/')
@render_to('list.html')
def rating_list(request):
    ctx = {
        'ratings': get_rating_list(),
    }
    return ctx
