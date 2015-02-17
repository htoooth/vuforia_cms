# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cms.models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0014_auto_20150217_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='image',
            field=models.ImageField(verbose_name='マーカー', upload_to=cms.models.Content.get_image_path, blank=True, null=True),
        ),
    ]
