# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cms.models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0009_auto_20150212_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='image',
            field=models.ImageField(upload_to=cms.models.Content.get_image_path, verbose_name='マーカー', null=True),
        ),
    ]
