# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-30 12:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_tournament_ended_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='stage',
            name='ended_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
