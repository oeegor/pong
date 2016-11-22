# coding: utf-8

from datetime import datetime, timedelta

from django.test import TestCase
from unittest.mock import patch

from account.models import User
from core.models import Group, SetResult, Stage, Tournament


class TestLogic(TestCase):

    @patch("core.models.send_templated_mail")
    def test_splits(self, *args, **kwargs):

        t = Tournament.objects.create(name="test")

        for i in range(16):
            username = "{}@test.tu".format(i)
            user = User.objects.create_user(username=username, email=username, password=username)
            t.participants.add(user)

        t.start()

        self.assertEqual(t.stages.all().count(), 1)
        self.assertEqual(t.stages.get().groups.all().count(), 4)

        next_stage = t.create_next_stage()
        self.assertEqual(t.stages.all().count(), 2)
        self.assertEqual(next_stage.groups.all().count(), 2)

        last_stage = t.create_next_stage()
        self.assertEqual(t.stages.all().count(), 3)
        self.assertEqual(last_stage.groups.all().count(), 1)

        with self.assertRaises(RuntimeError):
            t.create_next_stage()

    @patch("core.models.send_templated_mail")
    def test_user_actions(self, *args, **kwargs):

        t = Tournament.objects.create(name="test")
        s = Stage.objects.create(name="test", tournament=t, deadline=datetime.utcnow() + timedelta(days=1))
        g = Group.objects.create(name="test", stage=s)

        players = []
        for i in range(3):
            username = "{}@test.tu".format(i)
            user = User.objects.create_user(username=username, email=username, password=username)
            players.append(user)
            g.participants.add(user)

        SetResult.objects.create(group=g, player1_wins=True, player1_points=1, player2_points=1, player1=players[-1], player1_approved=True, player2=players[0])
        SetResult.objects.create(group=g, player1_wins=True, player1_points=1, player2_points=1, player2=players[-1], player1_approved=True, player1=players[1])

        actions = t.get_user_actions(players[-1])
        self.assertEqual(actions, [
            {'player': players[2], 'type': 'to_play'},
            {'player': players[1], 'type': 'approve'},
            {'player': players[0], 'type': 'ask_approval'},
        ])
