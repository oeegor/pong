# coding: utf-8

from datetime import datetime
from random import shuffle

from django.core.validators import MaxValueValidator
from django.db import models


class Table(list):
    def __init__(self, players, user_id):
        super(list, self).__init__()
        self.players = players
        for p1 in self.players:
            row = TableRow(players, p1, user_id)
            self.append(row)

    def set_places(self):
        sorted_rows = sorted(self, key=lambda i: i.points, reverse=True)
        for place, row in enumerate(sorted_rows, start=1):
            row.place = place


class TableRow(list):
    def __init__(self, players, player1, user_id):
        super(list, self).__init__()
        self.player1 = player1
        self.place = None
        for player2 in players:
            is_current_user = user_id in [player1.pk, player2.pk]
            self.append(TableCell(None, player1, player2, is_current_user))

    @property
    def balls(self):
        win = sum([s.score.balls_win for s in self if s.score])
        lose = sum([s.score.balls_lose for s in self if s.score])
        return u'{}:{}'.format(win, lose)

    @property
    def sets(self):
        win = sum([s.score.wins for s in self if s.score])
        lose = sum([s.score.loses for s in self if s.score])
        return u'{}:{}'.format(win, lose)

    @property
    def points(self):
        points = sum([s.score.points for s in self if s.score])
        return u'{}'.format(points)


class TableCell(object):
    def __init__(self, score, player1, player2, is_current_user):
        self.score = score
        self.player1 = player1
        self.player2 = player2
        self.is_approved = None
        self.is_current_user = is_current_user
        self.is_filler = player1.pk == player2.pk

    def __unicode__(self):
        return u'<Cell {}>'.format(self.score)

    def __repr__(self):
        return unicode(self)


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


class Tournament(models.Model):
    participants = models.ManyToManyField('account.User', blank=True)
    created_at = models.DateTimeField(default=datetime.utcnow)
    start_at = models.DateField()
    end_at = models.DateField(null=True, blank=True)

    def create_groups(self, capacity):
        if self.groups.all().exists():
            return
        names = ['Tech Ninjas', 'The Nerd Herd', 'The Awakening', 'United Ration']
        shuffle(names)
        players = self.participants.all().order_by('?')
        i = 0
        for player in players:
            if i == 0:
                group = Group.objects.create(
                    tournament=self,
                    name=names and names.pop(0) or 'noname',
                )
            group.participants.add(player)
            i += 1
            if i == capacity:
                i = 0

    def __unicode__(self):
        return u'Tournament {}| {}'.format(self.pk, self.start_at)


class Group(models.Model):
    name = models.CharField(max_length=256)
    tournament = models.ForeignKey('Tournament', related_name='groups')
    participants = models.ManyToManyField('account.User')
    created_at = models.DateTimeField(default=datetime.utcnow)

    def get_table(self, user_id):
        participants = self.participants.all().order_by('email')
        table = Table(participants, user_id)
        names = [p.short_email for p in participants]
        for r in self.results.all():
            i = names.index(r.player1.short_email)
            j = names.index(r.player2.short_email)
            table[i][j].set_result = table[j][i].set_result = r
            table[i][j].is_approved = table[j][i].is_approved = r.is_approved_by_user(user_id)
            table[i][j].score = r.get_score(True)
            table[j][i].score = r.get_score(False)
        table.set_places()
        print table
        return table

    def __unicode__(self):
        return u'Group {}| {}'.format(self.name, self.tournament)

    class Meta:
        unique_together = [('name', 'tournament')]


class SetResult(models.Model):
    group = models.ForeignKey('Group', related_name='results')

    player1 = models.ForeignKey('account.User', related_name='player1')
    player2 = models.ForeignKey('account.User', related_name='player2')

    player1_wins = models.PositiveSmallIntegerField(validators=[MaxValueValidator(3)])
    player1_points = models.PositiveSmallIntegerField(validators=[MaxValueValidator(11)])
    player2_points = models.PositiveSmallIntegerField(validators=[MaxValueValidator(11)])

    player1_approved = models.BooleanField(default=False)
    player2_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=datetime.utcnow)

    def is_approved_by_user(self, user_id):
        if user_id == self.player1_id:
            return self.player1_approved
        elif user_id == self.player2_id:
            return self.player2_approved
        else:
            return

    def get_score(self, is_player1):

        if is_player1:
            p1_wins = self.player1_wins
            p1_points = self.player1_points
            p2_points = self.player2_points
        else:
            p1_wins = 3 - self.player1_wins
            p1_points = self.player2_points
            p2_points = self.player1_points

        return Score(
            wins=p1_wins,
            balls_win=p1_points,
            balls_lose=p2_points,
        )

    def __unicode__(self):
        return u'SetResult {}| {}'.format(self.player1, self.player2)

    class Meta:
        unique_together = [('group', 'player1', 'player2')]


class Quote(models.Model):
    text = models.TextField()
    author = models.TextField(default='unknown')
    comment = models.TextField(null=True, blank=True)
