# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_auto_20150119_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 28, 14, 35, 33, 43929), editable=False, verbose_name='作成日'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='parent_agency_id',
            field=models.IntegerField(verbose_name='親AgencyID'),
        ),
    ]
