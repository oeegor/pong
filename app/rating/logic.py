# coding: utf-8
from rating.models import RatingHistory
from django.db import transaction


class PlayerRating(object):
    def __init__(self, player, rating, prev_rating):
        self.player = player
        self.rating = rating
        self.prev_rating = prev_rating


def get_player_rating(player, when):
    rt_q = RatingHistory.objects.filter(
        player=player,
        created_at__lte=when,
    ).order_by('-created_at')

    if not rt_q.exist():
        return PlayerRating(
            player, 0, 0
        )

    rt = list(rt_q.all()[0:2])

    res = PlayerRating(
        player,
        rt[0].rating,
        rt[1].rating,
    )

    return res


class RatingChange(object):
    def __init__(self, winner, looser, winner_rating, looser_rating, delta, when_changed):
        self.winner = winner
        self.looser = looser

        self.winner_rating = winner_rating
        self.looser_rating = looser_rating

        self.delta = delta

        self.when_changed = when_changed

    @property
    def new_winner_rating(self):
        return PlayerRating(
            player=self.winner,
            rating=self.winner_rating.rating + self.delta,
            prev_rating=self.winner_rating.rating,
        )

    @property
    def new_looser_rating(self):
        return PlayerRating(
            player=self.looser,
            rating=self.looser_rating.rating - self.delta,
            prev_rating=self.looser_rating.rating,
        )


def calculate_rating_changes(winner, looser, when_played):
    winner_rating = get_player_rating(winner, when_played)
    looser_rating = get_player_rating(looser, when_played)

    delta = 0

    if winner_rating.rating >= looser_rating.rating:
        rating_diff = winner_rating.rating - looser_rating.rating
        if rating_diff <= 2:
            delta = 2
        elif rating_diff <= 20:
            delta = 1
    else:
        delta = ((looser_rating.rating - winner_rating.rating) + 5) / 3

    return RatingChange(
        winner=winner,
        looser=looser,
        winner_rating=winner_rating,
        looser_rating=looser_rating,
        delta=delta,
        when_changed=when_played,
    )


def update_rating(rating_change):
    with transaction.atomic():
        RatingHistory.objects.create(
            player=rating_change.winner,
            created_at=rating_change.when_changed,
            rating=rating_change.new_winner_rating.rating,
        )
        RatingHistory.objects.create(
            player=rating_change.looser,
            created_at=rating_change.when_changed,
            rating=rating_change.new_looser_rating.rating,
        )
