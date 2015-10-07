# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0005_auto_20151006_1750'),
    ]

    operations = [
        migrations.CreateModel(
            name='SetResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('player1_wins', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(3)])),
                ('player1_points', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(11)])),
                ('player2_points', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(11)])),
                ('player1_approved', models.NullBooleanField()),
                ('player2_approved', models.NullBooleanField()),
                ('created_at', models.DateField(default=datetime.datetime.utcnow)),
            ],
        ),
        migrations.RemoveField(
            model_name='matchset',
            name='match',
        ),
        migrations.RemoveField(
            model_name='match',
            name='player1',
        ),
        migrations.RemoveField(
            model_name='match',
            name='player2',
        ),
        migrations.AlterField(
            model_name='group',
            name='tournament',
            field=models.ForeignKey(related_name='groups', to='core.Tournament'),
        ),
        migrations.AlterField(
            model_name='match',
            name='group',
            field=models.ForeignKey(related_name='matches', to='core.Group'),
        ),
        migrations.DeleteModel(
            name='MatchSet',
        ),
        migrations.AddField(
            model_name='setresult',
            name='group',
            field=models.ForeignKey(related_name='results', to='core.Group'),
        ),
        migrations.AddField(
            model_name='setresult',
            name='player1',
            field=models.ForeignKey(related_name='player1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='setresult',
            name='player2',
            field=models.ForeignKey(related_name='player2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='setresult',
            unique_together=set([('group', 'player1', 'player2')]),
        ),
    ]
