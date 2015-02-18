# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0019_auto_20150218_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(error_messages={'incomplete': '数字もしくはハイフンのみで入力してください。'}, max_length=16, verbose_name='電話番号', validators=[django.core.validators.RegexValidator('^[\\d-]+$', 'Enter a valid country calling code.')]),
        ),
    ]
