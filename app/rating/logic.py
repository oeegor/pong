# coding: utf-8
from account.models import User
from rating.models import RatingHistory
from django.db import transaction, connection


class PlayerRating(object):
    def __init__(self, player, rating):
        self.player = player
        self.rating = rating


def get_player_rating(player, when):
    rt_q = RatingHistory.objects.filter(
        player=player,
        created_at__lte=when,
    ).order_by('-created_at')

    if not rt_q.exists():
        return PlayerRating(
            player, 0
        )

    current_rating = rt_q[0].rating

    res = PlayerRating(
        player,
        current_rating,
    )

    return res


class RatingChange(object):
    def __init__(self, match, winner_rating, looser_rating, delta):
        self.match = match

        self.winner_rating = winner_rating
        self.looser_rating = looser_rating

        self.delta = delta

    @property
    def winner(self):
        return self.match.winner

    @property
    def looser(self):
        return self.match.looser

    @property
    def when_changed(self):
        return self.match.created_at


def calculate_rating_changes(match):
    assert match.is_approved

    winner_rating = get_player_rating(match.winner, match.created_at)
    looser_rating = get_player_rating(match.looser, match.created_at)

    delta = 0

    if winner_rating.rating >= looser_rating.rating:
        rating_diff = winner_rating.rating - looser_rating.rating
        if rating_diff <= 2:
            delta = 2
        elif rating_diff <= 20:
            delta = 1
    else:
        delta = ((looser_rating.rating - winner_rating.rating) + 5) / 3

    new_winner_rating = PlayerRating(
        player=match.winner,
        rating=winner_rating.rating + delta,
    )

    l_rt = looser_rating.rating - delta
    if l_rt < 0:
        l_rt = 0

    new_looser_rating = PlayerRating(
        player=match.looser,
        rating=l_rt,
    )

    return RatingChange(
        match=match,
        winner_rating=new_winner_rating,
        looser_rating=new_looser_rating,
        delta=delta,
    )


def update_rating(rating_change):
    with transaction.atomic():
        RatingHistory.objects.create(
            player=rating_change.winner,
            created_at=rating_change.when_changed,
            rating=rating_change.winner_rating.rating,
            match=rating_change.match,
        )
        RatingHistory.objects.create(
            player=rating_change.looser,
            created_at=rating_change.when_changed,
            rating=rating_change.looser_rating.rating,
            match=rating_change.match,
        )


def get_rating_list():
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

    users = {}
    for u in User.objects.filter(pk__in=ratings.keys()).all():
        users[u.pk] = u.username

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


class RatingHistoryItem(object):
    def __init__(self, player, match, delta, rating):
        self.player = player
        self.match = match
        self.delta = delta
        self.rating = rating

    @property
    def when(self):
        return self.match.created_at

    @property
    def is_winner(self):
        return self.player == self.match.winner

    @property
    def opponent(self):
        if self.is_winner:
            return self.match.looser
        else:
            return self.match.winner


def get_player_rating_history(player):
    res = []
    q = RatingHistory.objects.filter(player=player).select_related('match__player1', 'match__player2').order_by('created_at')
    cur_rt = 0
    for item in q:
        delta = abs(cur_rt - item.rating)
        cur_rt = item.rating
        res.append(
            RatingHistoryItem(
                player,
                item.match,
                delta=delta,
                rating=item.rating,
            )
        )

    return res
