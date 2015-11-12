# coding: utf-8

from account.models import User
from django.contrib.auth.decorators import login_required

from rating.logic import get_rating_list, get_player_rating_history
from utils import render_to


@login_required(login_url='/login/')
@render_to('list.html')
def rating_list(request):
    ctx = {
        'ratings': get_rating_list(),
    }
    return ctx


@login_required(login_url='/login/')
@render_to('player_history.html')
def rating_history(request, player_id):
    try:
        player = User.objects.get(pk=player_id)
    except User.DoesNotExist:
        return {}

    ctx = {
        'player': player,
        'history': reversed(get_player_rating_history(player)),
    }
    return ctx
