# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20151007_1342'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='group',
            unique_together=set([('name', 'tournament')]),
        ),
    ]
