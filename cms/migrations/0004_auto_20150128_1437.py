# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20150128_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 28, 14, 37, 45, 90276), editable=False, verbose_name='作成日'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='parent_agency_id',
            field=models.IntegerField(verbose_name='親AgencyID', null=True),
        ),
    ]
