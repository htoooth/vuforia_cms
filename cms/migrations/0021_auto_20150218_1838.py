# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0020_auto_20150218_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(validators=[django.core.validators.RegexValidator('^[\\d-]+$', '数字もしくはハイフンのみで入力してください。')], verbose_name='電話番号', max_length=16, error_messages={'incomplete': '数字もしくはハイフンのみで入力してください。'}),
        ),
    ]
