# coding: utf-8
from datetime import datetime

from django.db import models


class RatingHistory(models.Model):
    player = models.ForeignKey('account.User')
    match = models.ForeignKey('core.SetResult')
    rating = models.DecimalField(
        max_digits=7,
        decimal_places=1,
    )
    created_at = models.DateTimeField(default=datetime.utcnow)

    class Meta:
        unique_together = ('player', 'match')
