# -*- coding: utf-8 -*-
# Generated by Django 1.9b1 on 2015-11-12 13:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20151112_1359'),
        ('rating', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratinghistory',
            name='match',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.SetResult'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='ratinghistory',
            unique_together=set([('player', 'match')]),
        ),
    ]
