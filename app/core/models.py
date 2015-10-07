# coding: utf-8

from datetime import datetime
from itertools import combinations

from django.core.validators import MaxValueValidator
from django.db import models, transaction


class Table(list):
    def __init__(self, names):
        super(list, self).__init__()
        self.names = names

    def set_places(self):
        sorted_rows = sorted(self, key=lambda i: i.points, reverse=True)
        for place, row in enumerate(sorted_rows, start=1):
            row.place = place


class Score(object):
    def __init__(self, wins, balls_win, balls_lose):
        self.wins = wins
        self.balls_win = balls_win
        self.balls_lose = balls_lose

    def __unicode__(self):
        return u'<Score {}>'.format(self.score)

    def __repr__(self):
        return unicode(self)

    @property
    def loses(self):
        return 3 - self.wins

    @property
    def points(self):
        return int(bool(self.wins > self.loses))

    @property
    def score(self):
        return u'{}:{}'.format(self.wins, self.loses)


class TableRow(list):
    def __init__(self, size, name):
        super(list, self).__init__()
        self.name = name
        self.place = None
        for _ in xrange(size):
            self.append(None)

    @property
    def balls(self):
        win = sum([s.balls_win for s in self if s])
        lose = sum([s.balls_lose for s in self if s])
        return u'{}:{}'.format(win, lose)

    @property
    def sets(self):
        win = sum([s.wins for s in self if s])
        lose = sum([3 - s.wins for s in self if s])
        return u'{}:{}'.format(win, lose)

    @property
    def points(self):
        points = sum([s.points for s in self if s])
        return u'{}'.format(points)


class Tournament(models.Model):
    participants = models.ManyToManyField('account.User', blank=True)
    created_at = models.DateTimeField(default=datetime.utcnow)
    start_at = models.DateField()
    end_at = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return u'Tournament {}| {}'.format(self.pk, self.start_at)


class Group(models.Model):
    name = models.CharField(max_length=256)
    tournament = models.ForeignKey('Tournament', related_name='groups')
    participants = models.ManyToManyField('account.User')
    created_at = models.DateTimeField(default=datetime.utcnow)

    def get_table(self):
        matches = self.matches.all().order_by('player1__email')
        if not matches:
            self.generate_matches()

        # init table
        names = list(sorted({p.short_email for p in self.participants.all()}))
        table = Table(names)
        for name in names:
            table.append(TableRow(len(names), name))

        for m in matches:
            i = names.index(m.player1.short_email)
            j = names.index(m.player2.short_email)
            table[i][j] = m.get_score(i < j)
            table[j][i] = m.get_score(i > j)
        table.set_places()
        print table
        return table

    @transaction.atomic
    def generate_matches(self):
        matches = list(self.matches.all())
        if matches:
            return matches
        for p1, p2 in combinations(self.participants.all(), 2):
            matches.append(Match.objects.create(player1=p1, player2=p2, group=self))
        return matches

    def __unicode__(self):
        return u'Group {}| {}'.format(self.name, self.tournament)


class Match(models.Model):
    player1 = models.ForeignKey('account.User', related_name='player1')
    player2 = models.ForeignKey('account.User', related_name='player2')
    group = models.ForeignKey('Group', related_name='matches')
    created_at = models.DateTimeField(default=datetime.utcnow)

    def get_score(self, is_player1):
        wins = win_points = lose_points = 0
        results = self.results.all()
        if results.count() != 3:
            return None
        for result in results:
            if is_player1:
                p1_points = result.player1_points
                p2_points = result.player2_points
            else:
                p1_points = result.player2_points
                p2_points = result.player1_points

            if p1_points > p2_points:
                wins += 1
            win_points += p1_points
            lose_points += p2_points
        return Score(
            wins=wins,
            balls_win=win_points,
            balls_lose=lose_points
        )

    def __unicode__(self):
        return u'Match {}| {}'.format(self.player1, self.player2)


class MatchSet(models.Model):
    match = models.ForeignKey('Match', related_name='results')
    player1_points = models.PositiveSmallIntegerField(validators=[MaxValueValidator(11)])
    player1_approved = models.NullBooleanField()
    player2_points = models.PositiveSmallIntegerField(validators=[MaxValueValidator(11)])
    player2_approved = models.NullBooleanField()
    created_at = models.DateField(default=datetime.utcnow)

    def save(self, **kwargs):
        if self.pk is None and MatchSet.objects.filter(match=self.match).count() >= 3:
            raise ValueError('max number of match sets can be three')
        return super(MatchSet, self).save(**kwargs)
