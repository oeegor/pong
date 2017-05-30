# coding: utf-8

from datetime import timedelta
from logging import getLogger
import random

from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models, transaction
from django.utils import timezone

from core.vmodels import Score, Table
from helpers.mail import send_templated_mail
from utils import split_players_to_groups


logger = getLogger("core.models")


class Tournament(models.Model):
    participants = models.ManyToManyField('account.User', blank=True)
    name = models.CharField(max_length=256)
    start_at = models.DateField(null=True, blank=True)
    started_at = models.DateField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def start(self):
        if self.started_at is not None:
            raise RuntimeError("tournament has already started")
        if self.stages.all().count() > 0:
            raise RuntimeError("tournament has already started")

        self.create_stage(
            stage_name="First",
            participants=self.participants.all(),
        )

    def end(self):
        self.ended_at = timezone.now()
        self.save(update_fields=['ended_at'])
        self.send_tournament_ended_email()

    def create_next_stage(self):
        stage = self.stages.filter(ended_at__isnull=True).first()
        if not stage:
            raise RuntimeError("cannot find stage to start from")

        groups = list(stage.groups.all())
        if len(groups) == 1:
            stage.ended_at = timezone.now()
            stage.save(update_fields=["ended_at"])
            self.end()
            return

        players = []
        for group in groups:
            table = group.get_table()
            limit = int(len(table) / 2)
            for row in table[:limit]:
                players.append(row.player1)

        random.shuffle(players)
        next_stage = self.create_stage(
            stage_name=Stage.objects.filter(tournament=stage.tournament).count() + 1,
            participants=players,
        )
        stage.next_stage = next_stage
        stage.ended_at = timezone.now()
        stage.save(update_fields=["next_stage", "ended_at"])
        return next_stage

    def create_stage(self, stage_name, participants):
        stage = Stage.objects.create(
            deadline=timezone.now() + timedelta(days=14),
            name=stage_name,
            tournament=self,
        )

        for p in participants:
            stage.participants.add(p)

        stage.create_groups()
        stage.send_stage_created_email()
        return stage

    def get_user_actions(self, user):
        actions = []

        active_stage = self.get_active_stage()
        if not active_stage:
            return actions

        group = active_stage.groups.filter(participants__in=[user]).first()
        if not group:
            return actions

        query = models.Q(player1=user) | models.Q(player2=user)
        played_with = [
            r.player1 if r.player1 != user else r.player2
            for r in group.results.filter(query)
        ]

        # set with whon a user needs to play
        for p in group.participants.all():
            if p not in played_with:
                actions.append({"type": "to_play", "player": p})

        # set what a user needs to approve
        query = (
            models.Q(player1=user, player1_approved=False) |
            models.Q(player2=user, player2_approved=False)
        )
        for r in group.results.filter(query):
            player = r.player1 if r.player1 != user else r.player2
            actions.append({"type": "approve", "player": player})

        # set what another player should approve for this user
        query = (
            models.Q(player1=user, player2_approved=False) |
            models.Q(player2=user, player1_approved=False)
        )
        for r in group.results.filter(query):
            player = r.player1 if r.player1 != user else r.player2
            actions.append({"type": "ask_approval", "player": player})

        return actions

    def get_active_stage(self):
        stage = self.stages.filter(
            ended_at__isnull=True,
            next_stage__isnull=True,
        ).first()
        return stage

    def send_tournament_ended_email(self):
        stage = self.stages.all().order_by("-pk").first()
        group = stage.groups.all().prefetch_related('participants').first()

        mails = [p.email for p in self.participants.all()]
        template_name = 'tournament_has_ended'
        try:
            send_templated_mail(
                template_name=template_name,
                context={'group': {'name': group.name, 'table': group.get_table()}},
                recipients=mails,
                sender='donotreply-pongota@ostrovok.ru',
            )
        except TemplateDoesNotExist:
            logger.error("no template for {}".format(template_name), exc_info=True)

    def __str__(self):
        return 'Tournament {}| {}'.format(self.pk, self.name)


class Group(models.Model):
    name = models.CharField(max_length=256)
    participants = models.ManyToManyField('account.User')
    stage = models.ForeignKey("Stage", related_name="groups")
    created_at = models.DateTimeField(default=timezone.now)

    def get_table(self, user_id=None):
        participants = self.participants.all().order_by('email')
        table = Table(self, user_id)
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
        return 'Group {}| {}'.format(self.name, self.stage)

    class Meta:
        unique_together = [('stage', 'name')]


class Stage(models.Model):

    name = models.CharField(max_length=256)
    tournament = models.ForeignKey('Tournament', related_name='stages')
    created_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField()
    next_stage = models.OneToOneField("self", null=True, blank=True)
    participants = models.ManyToManyField("account.User", blank=True)

    @transaction.atomic
    def create_groups(self):
        if self.groups.all().exists():
            raise RuntimeError("groups are already created for this stage")

        stage_participants = list(self.participants.all().order_by('?'))
        if len(stage_participants) == 0:
            raise RuntimeError("cannot create groups for empty stage")

        groups = split_players_to_groups(stage_participants)
        for idx, group in enumerate(groups):
            dj_group = Group.objects.create(
                stage=self,
                name=chr(97 + idx).upper(),
            )
            dj_group.participants.add(*group)

    def send_stage_created_email(self):
        for group in self.groups.all().prefetch_related('participants'):
            mails = [p.email for p in group.participants.all()]

            subject = u'[pong] New Stage: {name}'.format(name=self.name)
            send_templated_mail(
                subject=subject,
                template_name='stage_has_been_created.html',
                context={'group': {'name': group.name, 'table': group.get_table()}},
                recipients=mails,
                sender='donotreply-pongota@ostrovok.ru',
            )

    @property
    def is_closed(self):
        return self.next_stage or self.deadline < timezone.now()

    def __str__(self):
        return 'Stage {}| {}'.format(self.name, self.tournament)

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

    created_at = models.DateTimeField(default=timezone.now)

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

    def get_score(self):
        p1_wins = self.player1_wins
        p1_points = self.player1_points
        p2_points = self.player2_points

        return Score(
            wins=p1_wins,
            balls_win=p1_points,
            balls_lose=p2_points,
            is_approved=self.is_approved,
        )

    def send_new_score_notification(self, approve_base_url):
        mails = [p.email for p in self.group.participants.all()]
        group = self.group

        subject = u'New result ({score} {player1_name}:{player2_name}) added!'.format(
            score=self.get_score(is_player1=True).score,
            player1_name=self.player1.short_email,
            player2_name=self.player2.short_email,
        )
        send_templated_mail(
            subject=subject,
            template_name='new_result_added.html',
            context={
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

        subject = u'Approve needed: ({score}  {player1_name}:{player2_name})'.format(
            score=self.get_score(is_player1=True).score,
            player1_name=self.player1.short_email,
            player2_name=self.player2.short_email,
        )
        send_templated_mail(
            subject=subject,
            template_name='need_result_approve.html',
            context={
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
