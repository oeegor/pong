# coding: utf-8

from functools import wraps
from itertools import cycle
from random import shuffle

from django.shortcuts import render


def render_to(tpl):
    def decorator(func):
        @wraps(func)
        def wrr(request, *args, **kwargs):
            result = func(request, *args, **kwargs)
            if isinstance(result, dict):
                result['quote'] = get_random_quote()
                rendered = render(request, tpl, result)
            else:
                rendered = result
            return rendered
        return wrr
    return decorator


def get_random_quote():
    from core.models import Quote
    return Quote.objects.all().order_by('?').first()


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]


def split_players_to_groups(players: list) -> list:
    min_group_len = 4
    if min_group_len >= len(players):
        return [players]
    all_groups = []
    for i in range(min_group_len, len(players)):
        groups = list(chunks(players, i))
        all_groups.append({
            "cap": i,
            "groups": groups,
            "k": abs(1 - float(i)/len(groups)),
        })

    groups = min(all_groups, key=lambda i: i["k"])
    print(groups)
    final_groups = []
    for group in groups["groups"]:
        if len(group) != groups["cap"]:
            group_cycle = cycle(final_groups)
            for i, player in enumerate(group):
                next(group_cycle).append(player)
        else:
            final_groups.append(group)
    return final_groups
