# coding: utf-8
import logging

from django.core.management.base import BaseCommand

from rating.models import RatingHistory
from core.models import SetResult
from rating.logic import calculate_rating_changes, update_rating


logger = logging.getLogger('debug')


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info('Starting ratings recalculate')

        self.drop_old_ratings()
        self.recalculate()

        logger.info('Done!')

    def drop_old_ratings(self):
        logger.info('Dropping old ratings')
        deleted, _ = RatingHistory.objects.all().delete()
        logger.info('Droppped {} records from history'.format(deleted))

    def recalculate(self):
        q = SetResult.objects.select_related('player1', 'player2').order_by('created_at')

        for match in q.all():
            if not match.is_approved:
                continue

            rating_change = calculate_rating_changes(match)
            logger.info(
                'Change after match on {when} between {winner} and {looser}. '
                '{winner} gets {delta} and now {winner_rating}. {looser} looses {delta} and now {looser_rating}'.format(
                    winner=rating_change.winner.username,
                    looser=rating_change.looser.username,
                    when=rating_change.when_changed,
                    delta=rating_change.delta,
                    winner_rating=rating_change.new_winner_rating.rating,
                    looser_rating=rating_change.new_looser_rating.rating,
                )
            )
            update_rating(rating_change)
