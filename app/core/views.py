# coding: utf-8

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponseRedirect

from account.models import User
from core.forms import SetResultForm
from core.models import SetResult, Tournament
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
    groups = [{
        'name': g.name,
        'table': g.get_table(request.user.pk),
        'pk': g.pk,
        } for g in t.groups.all()
    ]
    ctx = {
        'tournament': t,
        'groups': groups,
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
            initial={
                'group': group_id,
                'player1': player1_id,
                'player2': player2_id,
                'player1_approved': player1_id == str(request.user.pk),
                'player2_approved': player2_id == str(request.user.pk),
            },
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
        new_result = form.save()
        new_result.send_group_notification()
        return HttpResponseRedirect(reverse('app-tournament', args=[tournament_id]))


@login_required(login_url='/login/')
def approve_set_result(request, set_result_id):
    sr = SetResult.objects.filter(pk=set_result_id).first()
    if sr:
        user_id = request.user.pk
        if sr.player1.pk == user_id:
            sr.player1_approved = True
            sr.save()
        elif sr.player2.pk == user_id:
            sr.player2_approved = True
            sr.save()
    return HttpResponseRedirect(reverse('app-tournament', args=[sr.group.tournament.pk]))
