# coding: utf-8

import math
import random

from django.contrib import admin
from django.db import transaction

from .models import Group, Quote, Tournament, SetResult
from utils import split_players_to_groups


@transaction.atomic
def cherrypick_from_groups(modeladmin, request, queryset):
    players = []

    for group in queryset:
        table = group.get_table()
        limit = int(len(table) / 2)
        for row in table[:limit]:
            players.append(row.player1)
    else:
        tournament = group.tournament

    random.shuffle(players)
    groups = split_players_to_groups(players)
    for idx, group in enumerate(groups):
        dj_group = Group.objects.create(
            tournament=tournament,
            name=chr(97 + idx).upper()*2,
        )
        dj_group.participants.add(*group)
cherrypick_from_groups.short_description = "Cherrypick from groups"


def create_groups(modeladmin, request, queryset):
    for tournament in queryset:
        tournament.create_groups()
        tournament.send_tournament_started_email()
create_groups.short_description = "Generate groups"


class TournamentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'started_at', 'end_at')
    actions = [create_groups]


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'tournament')
    list_filter = ["tournament"]
    list_display_links = ('pk', 'tournament',)
    actions = [cherrypick_from_groups]


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author')


class SetResultAdmin(admin.ModelAdmin):
    list_display = ('player1', 'player2', 'player1_points', 'player2_points', 'player1_approved', 'player2_approved', 'group', 'created_at')
    list_filter = ('player1', 'player2', 'player1_points', 'player2_points', 'player1_approved', 'player2_approved', 'group')
    list_display_links = ('group', 'player1', 'player2')


admin.site.register(Group, GroupAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(SetResult, SetResultAdmin)
