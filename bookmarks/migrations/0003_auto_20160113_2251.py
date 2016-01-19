# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0002_auto_20160113_2249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookmark',
            old_name='url',
            new_name='task',
        ),
    ]
