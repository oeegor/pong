# coding: utf-8

from datetime import date, datetime

from dj_templated_mail.logic import send_templated_mail
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models, transaction

from utils import split_players_to_groups


class Table(list):
    def __init__(self, players, user_id):
        super().__init__()
        self.players = players
        for p1 in self.players:
            row = TableRow(players, p1, user_id)
            self.append(row)

    def set_places(self):
        def key(i):
            return (int(i.points), int(i.sets.split(":")[0]), int(i.balls.split(":")[0]))
        self.sort(key=key, reverse=True)
        for place, row in enumerate(self, start=1):
            row.place = place


class TableRow(list):
    def __init__(self, players, player1, user_id):
        super().__init__()
        self.player1 = player1
        self.place = None
        for player2 in players:
            is_current_user = user_id in [player1.pk, player2.pk]
            self.append(TableCell(None, player1, player2, is_current_user))

    @property
    def balls(self):
        win = sum([s.score.balls_win for s in self if s.score])
        lose = sum([s.score.balls_lose for s in self if s.score])
        return '{}:{}'.format(win, lose)

    @property
    def sets(self):
        win = sum([s.score.wins for s in self if s.score])
        lose = sum([s.score.loses for s in self if s.score])
        return '{}:{}'.format(win, lose)

    @property
    def points(self):
        points = sum([s.score.points for s in self if s.score])
        return '{}'.format(points)


class TableCell(object):
    def __init__(self, score, player1, player2, is_current_user):
        self.score = score
        self.player1 = player1
        self.player2 = player2
        self.is_approved = None
        self.is_current_user = is_current_user
        self.is_filler = player1.pk == player2.pk

    def __str__(self):
        return '<Cell {}>'.format(self.score)

    def __repr__(self):
        return str(self)


class Score(object):
    def __init__(self, wins, balls_win, balls_lose, is_approved):
        self.wins = wins
        self.balls_win = balls_win
        self.balls_lose = balls_lose
        self.is_approved = is_approved

    def __str__(self):
        return '<Score {}>'.format(self.score)

    def __repr__(self):
        return str(self)

    @property
    def loses(self):
        return 3 - self.wins

    @property
    def points(self):
        return int(bool(self.wins > self.loses)) if self.is_approved else 0

    @property
    def score(self):
        return '{}:{}'.format(self.wins, self.loses)

    @property
    def balls(self):
        return '{}:{}'.format(self.balls_win, self.balls_lose)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


class Tournament(models.Model):
    participants = models.ManyToManyField('account.User', blank=True)
    created_at = models.DateTimeField(default=datetime.utcnow)
    name = models.CharField(max_length=256)
    started_at = models.DateField(null=True, blank=True)
    end_at = models.DateField(null=True, blank=True)

    @transaction.atomic
    def create_groups(self):
        if self.groups.all().exists():
            return
        players = list(self.participants.all().order_by('?'))
        groups = split_players_to_groups(players)
        for idx, group in enumerate(groups):
            dj_group = Group.objects.create(
                tournament=self,
                name=chr(97 + idx).upper(),
            )
            dj_group.participants.add(*group)

        self.started_at = date.today()
        self.save(update_fields=['started_at'])

    def send_tournament_started_email(self):
        for group in self.groups.all().prefetch_related('participants'):
            mails = [p.email for p in group.participants.all()]
            send_templated_mail(
                template_name='tournament_has_started',
                context={'group': {'name': group.name, 'table': group.get_table()}},
                recipients=mails,
                sender='donotreply-pongota@ostrovok.ru',
            )

    def __str__(self):
        return 'Tournament {}| {}'.format(self.pk, self.name)


class Group(models.Model):
    name = models.CharField(max_length=256)
    tournament = models.ForeignKey('Tournament', related_name='groups')
    participants = models.ManyToManyField('account.User')
    created_at = models.DateTimeField(default=datetime.utcnow)

    def get_table(self, user_id=None):
        participants = self.participants.all().order_by('email')
        table = Table(participants, user_id)
        names = [p.short_email for p in participants]
        for r in self.results.all():
            i = names.index(r.player1.short_email)
            j = names.index(r.player2.short_email)
            table[i][j].set_result = table[j][i].set_result = r
            is_approved = r.is_approved
            if user_id and user_id not in [r.player1.pk, r.player2.pk]:
                is_approved = True

            table[i][j].is_approved = table[j][i].is_approved = is_approved
            table[i][j].score = r.get_score(True)
            table[j][i].score = r.get_score(False)
        table.set_places()
        return table

    def __str__(self):
        return 'Group {}| {}'.format(self.name, self.tournament)

    class Meta:
        unique_together = [('name', 'tournament')]


class SetResult(models.Model):
    group = models.ForeignKey(
        'Group',
        null=True, blank=True,
        related_name='results'
    )

    player1 = models.ForeignKey('account.User', related_name='player1')
    player2 = models.ForeignKey('account.User', related_name='player2')

    player1_wins = models.PositiveSmallIntegerField(validators=[MaxValueValidator(3)])
    player1_points = models.PositiveSmallIntegerField(validators=[MaxValueValidator(33)])
    player2_points = models.PositiveSmallIntegerField(validators=[MaxValueValidator(33)])

    player1_approved = models.BooleanField(default=False)
    player2_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=datetime.utcnow)

    @property
    def is_approved(self):
        return self.player1_approved and self.player2_approved

    @property
    def winner(self):
        if self.player1_wins > 1:
            return self.player1
        else:
            return self.player2

    @property
    def looser(self):
        if self.player1_wins < 2:
            return self.player1
        else:
            return self.player2

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
            is_approved=self.is_approved,
        )

    def send_group_notification(self, approve_base_url):
        mails = [p.email for p in self.group.participants.all()]
        group = self.group
        send_templated_mail(
            template_name='new_result_added',
            context={
                'player1_name': self.player1.short_email,
                'player2_name': self.player2.short_email,
                'score': self.get_score(is_player1=True).score,
                'group': {'name': group.name, 'table': group.get_table()},
                'approve_base_url': approve_base_url,
            },
            recipients=mails,
            sender='donotreply-pongota@ostrovok.ru',
        )

    def send_approve_notification(self, sender_id):
        opponent = self.player1
        if self.player1.pk == sender_id:
            opponent = self.player2

        mails = [opponent.email]
        send_templated_mail(
            template_name='need_result_approve',
            context={
                'player1_name': self.player1.short_email,
                'player2_name': self.player2.short_email,
                'score': self.get_score(is_player1=True).score,
                'match_id': self.pk,
            },
            recipients=mails,
            sender=settings.EMAIL_HOST_USER,
        )

    def __str__(self):
        return 'SetResult {}| {}'.format(self.player1, self.player2)

    class Meta:
        unique_together = [('group', 'player1', 'player2')]


class Quote(models.Model):
    text = models.TextField()
    author = models.TextField(default='unknown')
    comment = models.TextField(null=True, blank=True)
