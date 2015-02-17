# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0015_auto_20150217_1545'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': (('running', 'can log in'),), 'verbose_name': 'ユーザー', 'verbose_name_plural': 'ユーザー'},
        ),
    ]
