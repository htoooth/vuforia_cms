# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0017_auto_20150217_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='mapping_url',
            field=models.URLField(null=True, max_length=128, verbose_name='マッピングURL'),
        ),
    ]
