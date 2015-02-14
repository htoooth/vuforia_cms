# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cms.models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0011_auto_20150214_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='image',
            field=models.ImageField(upload_to=cms.models.Content.get_image_path, null=True, blank=True, verbose_name='マーカー'),
        ),
        migrations.AlterField(
            model_name='content',
            name='target_id',
            field=models.CharField(null=True, max_length=128, verbose_name='ターゲットID'),
        ),
    ]
