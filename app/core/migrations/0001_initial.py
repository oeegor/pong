# -*- coding: utf-8 -*-


from django.db import migrations, models
import datetime
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.utcnow)),
            ],
        ),
        migrations.CreateModel(
            name='MatchSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('player1_points', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(11)])),
                ('player1_oved', models.NullBooleanField()),
                ('player2_points', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(11)])),
                ('player2_oved', models.NullBooleanField()),
                ('match', models.ForeignKey(to='core.Match')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('start_at', models.DateField()),
                ('end_at', models.DateField(null=True, blank=True)),
                ('participants', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='Tournament',
            field=models.ForeignKey(to='core.Tournament'),
        ),
        migrations.AddField(
            model_name='match',
            name='player1',
            field=models.ForeignKey(related_name='player1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='match',
            name='player2',
            field=models.ForeignKey(related_name='player2', to=settings.AUTH_USER_MODEL),
        ),
    ]
