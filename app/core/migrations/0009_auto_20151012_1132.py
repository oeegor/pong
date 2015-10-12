# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20151007_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setresult',
            name='player1_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='setresult',
            name='player2_approved',
            field=models.BooleanField(default=False),
        ),
    ]
