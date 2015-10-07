# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20151006_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='group',
            field=models.ForeignKey(to='core.Group'),
        ),
    ]
