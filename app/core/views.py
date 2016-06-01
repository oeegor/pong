# coding: utf-8
from copy import deepcopy

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponseBadRequest

from account.models import User
from core.forms import SetResultForm
from core.models import SetResult, Tournament
from rating.logic import calculate_rating_changes, update_rating
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
    url = "%s://%s:%s" % (request.scheme, request.get_host(), request.get_port())
    ctx = {
	'approve_base_url': url,
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
    player1 = User.objects.get(pk=player1_id)
    player2 = User.objects.get(pk=player2_id)
    if request.method == 'GET':
        initial = {
            'player1': player1_id,
            'player2': player2_id,
            'player1_approved': player1_id == str(request.user.pk),
            'player2_approved': player2_id == str(request.user.pk),
        }
        if group_id:
            initial['group'] = group_id
        form = SetResultForm(
            initial=initial,
        )
        form.set_inputs(player1=player1, player2=player2)
        ctx = {
            'form': form
        }
        return ctx

    elif request.method == 'POST':
        post_data = deepcopy(request.POST)
        if post_data['group'] == '0':
            del post_data['group']
        form = SetResultForm(post_data)
        if str(request.user.pk) not in [player1_id, player2_id]:
            form.add_error(None, 'cannot set scores for not your games')
        if not form.is_valid():
            form.set_inputs(player1=player1, player2=player2)
            return {
                'form': form
            }
        new_result = form.save()
        if 'group' in post_data:
            url = "%s://%s:%s" % (request.scheme, request.get_host(), request.get_port())
            new_result.send_group_notification(approve_base_url=url)
        else:
            new_result.send_approve_notification(request.user.pk)

        if int(tournament_id):
            return HttpResponseRedirect(reverse('app-tournament', args=[tournament_id]))
        else:
            return HttpResponseRedirect(reverse('rating-list'))


@login_required(login_url='/login/')
def approve_set_result(request, set_result_id):
    sr = SetResult.objects.filter(pk=set_result_id).first()
    if not sr:
        return HttpResponseBadRequest('Match with id {} does not exist'.format(set_result_id))

    user_id = request.user.pk
    if sr.player1.pk != user_id and sr.player2.pk != user_id:
        return HttpResponseBadRequest('You are not the participant of the match {}'.format(set_result_id))

    if sr.is_approved:
        return HttpResponseBadRequest('Match already approved')

    with transaction.atomic():
        if sr.player1.pk == user_id:
            sr.player1_approved = True
        elif sr.player2.pk == user_id:
            sr.player2_approved = True

        sr.save()

        if sr.is_approved:
            rating_changes = calculate_rating_changes(sr)
            update_rating(rating_changes)

    if sr.group:
        return HttpResponseRedirect(reverse('app-tournament', args=[sr.group.tournament.pk]))
    else:
        return HttpResponseRedirect(reverse('rating-list'))
