# coding: utf-8

from django.contrib import admin

from .models import Group, Tournament, SetResult


class TournamentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'start_at', 'end_at')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'tournament')
    list_display_links = ('tournament',)


class SetResultAdmin(admin.ModelAdmin):
    list_display = ('player1', 'player2', 'player1_points', 'player2_points', 'player1_approved', 'player2_approved', 'group', 'created_at')
    list_filter = ('player1', 'player2', 'player1_points', 'player2_points', 'player1_approved', 'player2_approved', 'group')
    list_display_links = ('group', 'player1', 'player2')


admin.site.register(Group, GroupAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(SetResult, SetResultAdmin)
