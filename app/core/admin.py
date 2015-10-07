# coding: utf-8

from django.contrib import admin

from .models import Group, Tournament, Match, MatchSet


class TournamentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'start_at', 'end_at')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'tournament')
    list_display_links = ('tournament',)


class MatchAdmin(admin.ModelAdmin):
    list_display = ('player1', 'player2', 'group', 'created_at')
    list_filter = ('player1', 'player2', 'group')
    list_display_links = ('group',)


class MatchSetAdmin(admin.ModelAdmin):
    exclude = ('last_sent_at',)
    list_display = ('match', 'player1_points', 'player2_points', 'player1_approved', 'player2_approved',)
    list_display = ('match', 'player1_points', 'player2_points', 'player1_approved', 'player2_approved',)
    search_fields = ('message', 'custom_payload')
    list_display_links = ('match',)


admin.site.register(Group, GroupAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(MatchSet, MatchSetAdmin)
