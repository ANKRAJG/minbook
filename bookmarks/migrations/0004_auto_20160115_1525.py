# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0003_auto_20160113_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='task',
            field=models.URLField(),
        ),
    ]
