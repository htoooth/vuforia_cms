# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_auto_20150214_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='open_to',
            field=models.DateField(null=True, verbose_name='公開期間 至', blank=True),
        ),
    ]
