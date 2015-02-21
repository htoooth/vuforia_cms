# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0021_auto_20150218_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_id',
            field=models.PositiveIntegerField(verbose_name='ユーザーID', null=True),
        ),
    ]
