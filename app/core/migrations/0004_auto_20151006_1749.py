# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20151006_1743'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='tournament',
        ),
        migrations.AddField(
            model_name='match',
            name='group',
            field=models.ForeignKey(to='core.Group', null=True),
        ),
    ]
