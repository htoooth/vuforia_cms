# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0007_auto_20150211_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='image',
            field=models.ImageField(null=True, upload_to='images'),
            preserve_default=True,
        ),
    ]
