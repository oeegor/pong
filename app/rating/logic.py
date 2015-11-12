# coding: utf-8
from account.models import User
from rating.models import RatingHistory
from django.db import transaction, connection


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


def get_rating_list():
    users = {}
    for u in User.objects.all():
        users[u.pk] = u.username

    cursor = connection.cursor()

    cursor.execute(
        """
            SELECT DISTINCT ON(player_id)
              player_id,
                rating
            FROM rating_ratinghistory
            ORDER BY player_id, created_at DESC
        """
    )
    ratings = {}
    for player_id, rating in cursor.fetchall():
        ratings[player_id] = rating

    res = []
    for player_id, player_name in iter(users.items()):
        res.append({
            'player_id': player_id,
            'player_name': player_name,
            'player_rating': ratings.get(player_id, 0)
        })

    res = sorted(
        res,
        key=lambda pl: (pl['player_rating'] * -1, pl['player_name'])
    )

    return res
