# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-29 13:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20161129_0918'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='group',
            unique_together=set([('stage', 'name')]),
        ),
    ]
