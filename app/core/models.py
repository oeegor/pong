# coding: utf-8

from datetime import datetime

from django.core.validators import MaxValueValidator
from django.db import models


class Tournament(models.Model):
    participants = models.ManyToManyField('account.User')
    created_at = models.DateTimeField(default=datetime.utcnow)
    start_at = models.DateField()
    end_at = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return u'Tournament {}| {}'.format(self.pk, self.start_at)


class Match(models.Model):
    player1 = models.ForeignKey('account.User', related_name='player1')
    player2 = models.ForeignKey('account.User', related_name='player2')
    Tournament = models.ForeignKey('Tournament')
    created_at = models.DateTimeField(default=datetime.utcnow)

    def __unicode__(self):
        return u'Match {}| {}'.format(self.player1, self.player2)


class MatchSet(models.Model):
    match = models.ForeignKey('Match')
    player1_points = models.PositiveSmallIntegerField(validators=[MaxValueValidator(11)])
    player1_oved = models.NullBooleanField()
    player2_points = models.PositiveSmallIntegerField(validators=[MaxValueValidator(11)])
    player2_oved = models.NullBooleanField()

    def save(self, **kwargs):
        if self.pk is None and MatchSet.objects.filter(match=self.match).count() > 3:
            raise ValueError('max number of match sets can be three')
        return super(MatchSet, self).save(**kwargs)
