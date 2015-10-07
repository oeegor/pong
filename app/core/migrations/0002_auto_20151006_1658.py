# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='Tournament',
            new_name='tournament',
        ),
        migrations.RenameField(
            model_name='matchset',
            old_name='player1_oved',
            new_name='player1_approved',
        ),
        migrations.RenameField(
            model_name='matchset',
            old_name='player2_oved',
            new_name='player2_approved',
        ),
        migrations.AddField(
            model_name='matchset',
            name='created_at',
            field=models.DateField(default=datetime.datetime.utcnow),
        ),
    ]
