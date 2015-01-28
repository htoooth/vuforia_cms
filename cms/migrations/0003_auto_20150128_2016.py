# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_auto_20150128_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='contract_no',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='契約番号'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='created_at',
            field=models.DateTimeField(editable=False, default=datetime.datetime(2015, 1, 28, 20, 16, 34, 192748), verbose_name='作成日'),
        ),
    ]
