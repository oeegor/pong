# coding: utf-8

import math
import random

from django.contrib import admin
from django.db import transaction

from .models import Group, Quote, Stage, Tournament, SetResult
from utils import split_players_to_groups


@transaction.atomic
def create_next_stage(modeladmin, request, queryset):
    for tournament in queryset:
        tournament.create_next_stage()
create_next_stage.short_description = "Create the next stage"


@transaction.atomic
def create_first_stage(modeladmin, request, queryset):
    for tournament in queryset:
        tournament.start()
create_first_stage.short_description = "Create the first stage"


class TournamentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'start_at')
    actions = [create_first_stage, create_next_stage]


class StageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'tournament')
    list_filter = ["tournament"]
    list_display_links = ('pk', 'tournament',)


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
