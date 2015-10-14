# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_quote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournament',
            name='start_at',
        ),
        migrations.AddField(
            model_name='tournament',
            name='name',
            field=models.CharField(default='ostrovach', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tournament',
            name='started_at',
            field=models.DateField(null=True, blank=True),
        ),
    ]
