# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-30 13:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20161130_1332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournament',
            name='created_at',
        ),
        migrations.AddField(
            model_name='tournament',
            name='started_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
