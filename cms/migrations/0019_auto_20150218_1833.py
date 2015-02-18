# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0018_auto_20150218_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(verbose_name='電話番号', max_length=16, validators=[django.core.validators.RegexValidator('^[\\d-]+$', 'Enter a valid country calling code.')], error_messages={'incomplete': 'Enter a country calling code.'}),
        ),
    ]
