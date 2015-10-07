# coding: utf-8

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponseRedirect

from account.models import User
from core.forms import SetResultForm
from core.models import Tournament
from utils import render_to


@login_required(login_url='/login/')
@render_to('index.html')
def home(request):

    ctx = {
        'joined_tournaments': Tournament.objects.filter(participants=request.user),
        'available_tournaments': (
            Tournament.objects
            .exclude(participants=request.user)
            .annotate(group_cnt=Count('groups'))
            .exclude(group_cnt__gt=0)
        )
    }
    return ctx


@login_required(login_url='/login/')
@render_to('tournament.html')
def tournament(request, tournament_id):
    t = Tournament.objects.get(id=tournament_id)
    ctx = {
        'tournament': t,
        'groups': t.groups.all(),
        'participants': t.participants.all(),
    }
    return ctx


@login_required(login_url='/login/')
def join_tournament(request, tournament_id):
    t = Tournament.objects.get(id=tournament_id)
    t.participants.add(request.user)
    return tournament(request, t.pk)


@login_required(login_url='/login/')
@render_to('add_set_result.html')
def add_set_result(request, tournament_id, group_id, player1_id, player2_id):
    if request.method == 'GET':
        form = SetResultForm(
            initial={'group': group_id, 'player1': player1_id, 'player2': player2_id},
        )
        form.set_hidden_inputs()
        ctx = {
            'player1': User.objects.get(pk=player1_id),
            'player2': User.objects.get(pk=player2_id),
            'form': form
        }
        return ctx

    elif request.method == 'POST':
        form = SetResultForm(request.POST)
        if str(request.user.pk) not in [player1_id, player2_id]:
            form.add_error(None, 'cannot set scores for not your games')
        if not form.is_valid():
            form.set_hidden_inputs()
            return {
                'form': form
            }
        form.save()
        return HttpResponseRedirect(reverse('app-tournament', args=[tournament_id]))
