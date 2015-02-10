# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20150128_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='contracted_at',
            field=models.DateField(verbose_name='契約日', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='content',
            name='open_from',
            field=models.DateField(verbose_name='公開期間 自', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='content',
            name='open_to',
            field=models.DateField(null=True, verbose_name='公開期間 至'),
        ),
        migrations.AlterField(
            model_name='content',
            name='terminated_at',
            field=models.DateField(null=True, verbose_name='契約解除日'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='created_at',
            field=models.DateTimeField(editable=False, verbose_name='作成日', default=datetime.datetime(2015, 2, 11, 11, 35, 7, 590629)),
        ),
    ]
