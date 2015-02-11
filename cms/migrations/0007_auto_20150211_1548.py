# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0006_auto_20150211_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='company',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, verbose_name='Company'),
        ),
    ]
