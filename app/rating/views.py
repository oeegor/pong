# coding: utf-8

from account.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

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


@login_required(login_url='/login/')
@render_to('rated-game.html')
def rated_game_save(request):
    if request.method == 'GET':
        ctx = {
            'users': User.objects.order_by('username').exclude(pk=request.user.pk).all(),
        }
        return ctx
    elif request.method == 'POST':
        player_1_id = request.user.pk
        player_2_id = request.POST.get('opponent_id')
        return HttpResponseRedirect(
            reverse(
                'app-add-set-result',
                args=[0, 0, player_1_id, player_2_id]
            )
        )
