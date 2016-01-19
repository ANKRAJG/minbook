# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0004_auto_20160115_1525'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag_list',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('tags', models.CharField(max_length=100)),
            ],
        ),
    ]
