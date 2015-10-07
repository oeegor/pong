# coding: utf-8

from django.contrib import admin

from .models import Group, Tournament, SetResult


def create_groups_5(modeladmin, request, queryset):
    for tournament in queryset:
        tournament.create_groups(5)
create_groups_5.short_description = "Generate groups with 5 players"


def create_groups_4(modeladmin, request, queryset):
    for tournament in queryset:
        tournament.create_groups(4)
create_groups_4.short_description = "Generate groups with 4 players"


def create_groups_2(modeladmin, request, queryset):
    for tournament in queryset:
        tournament.create_groups(2)
create_groups_2.short_description = "Generate groups with 2 players"


def create_groups_6(modeladmin, request, queryset):
    for tournament in queryset:
        tournament.create_groups(6)
create_groups_6.short_description = "Generate groups with 6 players"


class TournamentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'start_at', 'end_at')
    actions = [create_groups_4, create_groups_5, create_groups_6, create_groups_2]


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'tournament')
    list_display_links = ('pk', 'tournament',)


class SetResultAdmin(admin.ModelAdmin):
    list_display = ('player1', 'player2', 'player1_points', 'player2_points', 'player1_approved', 'player2_approved', 'group', 'created_at')
    list_filter = ('player1', 'player2', 'player1_points', 'player2_points', 'player1_approved', 'player2_approved', 'group')
    list_display_links = ('group', 'player1', 'player2')


admin.site.register(Group, GroupAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(SetResult, SetResultAdmin)
