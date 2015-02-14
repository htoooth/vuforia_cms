# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0010_auto_20150213_0858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='target_id',
            field=models.CharField(verbose_name='ターゲットID', blank=True, max_length=128, null=True),
        ),
    ]
