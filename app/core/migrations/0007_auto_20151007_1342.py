# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20151007_1234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='group',
        ),
        migrations.AlterField(
            model_name='setresult',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.utcnow),
        ),
        migrations.DeleteModel(
            name='Match',
        ),
    ]
