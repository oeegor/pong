# coding: utf-8

import math
import random

from django.contrib import admin
from django.db import transaction

from .models import Group, Quote, Stage, Tournament, SetResult
from utils import split_players_to_groups


@transaction.atomic
def create_next_stage(modeladmin, request, queryset):
    for stage in queryset.exclude(next_stage__isnull=False):

        players = []
        for group in stage.groups.all():
            table = group.get_table()
            limit = int(len(table) / 2)
            for row in table[:limit]:
                players.append(row.player1)

        random.shuffle(players)
        groups = split_players_to_groups(players)
        for idx, group in enumerate(groups):
            next_stage = stage.tournament.create_stage(
                stage_name=Stage.objects.filter(tournament=stage.tournament).count() + 1,
                participants=group,
            )
            next_stage.create_groups()
            stage.next_stage = next_stage
            stage.save(update_fields=["next_stage"])
create_next_stage.short_description = "Create the next stage"


@transaction.atomic
def create_first_stage(modeladmin, request, queryset):
    for tournament in queryset:
        tournament.start()
create_first_stage.short_description = "Create the first stage"


class TournamentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'started_at', 'end_at')
    actions = [create_first_stage]


class StageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'tournament')
    list_filter = ["tournament"]
    list_display_links = ('pk', 'tournament',)
    actions = [create_next_stage]


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'stage')
    list_filter = ["stage", "stage__tournament"]
    list_display_links = ('pk', 'stage',)


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author')


class SetResultAdmin(admin.ModelAdmin):
    list_display = ('player1', 'player2', 'player1_points', 'player2_points', 'player1_approved', 'player2_approved', 'group', 'created_at')
    list_filter = ('player1', 'player2', 'player1_points', 'player2_points', 'player1_approved', 'player2_approved', 'group')
    list_display_links = ('group', 'player1', 'player2')


admin.site.register(Stage, StageAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(SetResult, SetResultAdmin)
