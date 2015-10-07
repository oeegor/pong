# coding: utf-8

from django.contrib.auth.decorators import login_required

from core.models import Tournament, Match
from utils import render_to


@login_required(login_url='/login/')
@render_to('index.html')
def home(request):

    ctx = {
        'joined_tournaments': Tournament.objects.filter(participants=request.user),
        'available_tournaments': Tournament.objects.exclude(participants=request.user)
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
@render_to('match.html')
def match(request, match_id):
    match = Match.objects.get(id=match_id)
    ctx = {
        'match': match,
    }
    return ctx
