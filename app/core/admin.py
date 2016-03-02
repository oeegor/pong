# coding: utf-8

from django.contrib import admin

from .models import Group, Quote, Tournament, SetResult


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
    list_display_links = ('pk', 'tournament',)


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
