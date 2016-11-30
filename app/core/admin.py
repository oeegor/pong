# coding: utf-8

from django.contrib import admin
from django.db import transaction

from .models import Group, Quote, Stage, Tournament, SetResult


@transaction.atomic
def create_next_stage(modeladmin, request, queryset):
    for tournament in queryset:
        tournament.create_next_stage()
create_next_stage.short_description = "Create the next stage"


@transaction.atomic
def start_tournament(modeladmin, request, queryset):
    for tournament in queryset:
        tournament.start()
start_tournament.short_description = "Start selected tournaments"


class TournamentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'start_at')
    actions = [start_tournament, create_next_stage]


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
