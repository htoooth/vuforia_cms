# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0005_auto_20150211_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='delete_flag',
            field=models.SmallIntegerField(verbose_name='論理削除', default=0),
        ),
        migrations.AlterField(
            model_name='content',
            name='mapping_url',
            field=models.CharField(verbose_name='マッピングURL', max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='recognition',
            field=models.SmallIntegerField(verbose_name='認識率', null=True, default=0),
        ),
        migrations.AlterField(
            model_name='content',
            name='target_id',
            field=models.CharField(verbose_name='ターゲットID', max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='title',
            field=models.CharField(verbose_name='タイトル', max_length=64, null=True),
        ),
    ]
