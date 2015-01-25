# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminuser',
            name='user_profile_id',
            field=models.IntegerField(verbose_name='AdminID', null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='agencyuser',
            name='user_profile_id',
            field=models.IntegerField(verbose_name='AgencyID', null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='companyuser',
            name='user_profile_id',
            field=models.IntegerField(verbose_name='CompanyID', null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='created_at',
            field=models.DateTimeField(editable=False, default=datetime.datetime(2015, 1, 19, 20, 43, 22, 113230), verbose_name='作成日'),
        ),
    ]
