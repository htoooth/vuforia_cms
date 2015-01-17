# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CmsUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField(verbose_name='ユーザーID')),
                ('acc_type_id', models.CharField(max_length=2, verbose_name='アカウントタイプID', choices=[(0, 'Admin'), (1, 'Agency'), (2, 'Company')])),
                ('pw', models.CharField(max_length=10, verbose_name='ログインパスワード')),
                ('parent_admin_id', models.IntegerField(default=0, verbose_name='親AdminID')),
                ('parent_agency_id', models.IntegerField(default=0, verbose_name='親AgencyID')),
                ('user_running', models.SmallIntegerField(default=0, verbose_name='稼働フラグ')),
                ('enterprise', models.CharField(max_length=64, verbose_name='企業名')),
                ('person', models.CharField(max_length=64, verbose_name='担当者名')),
                ('address', models.CharField(max_length=64, verbose_name='住所')),
                ('mail_address', models.EmailField(max_length=75, verbose_name='メールアドレス')),
                ('phone_number', models.CharField(max_length=16, verbose_name='電話番号')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 17, 21, 25, 12, 948793), verbose_name='作成日', editable=False)),
                ('updated_at', models.DateTimeField(verbose_name='更新日', editable=False)),
            ],
            options={
                'verbose_name': 'ユーザー',
                'verbose_name_plural': 'ユーザー',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('contract_no', models.PositiveIntegerField(verbose_name='契約番号', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64, verbose_name='タイトル')),
                ('target_id', models.CharField(max_length=128, verbose_name='ターゲットID')),
                ('mapping_url', models.CharField(max_length=128, verbose_name='マッピングURL')),
                ('open_from', models.CharField(max_length=16, verbose_name='公開期間 自')),
                ('open_to', models.CharField(max_length=16, verbose_name='公開期間 至', null=True)),
                ('is_open', models.SmallIntegerField(default=0, verbose_name='公開フラグ')),
                ('sort', models.IntegerField(default=0, verbose_name='ソートインデックス')),
                ('user_id', models.IntegerField(verbose_name='CompanyID')),
                ('recognition', models.SmallIntegerField(default=0, verbose_name='認識率')),
                ('contracted_at', models.CharField(max_length=16, verbose_name='契約日')),
                ('delete_flag', models.SmallIntegerField(default=1, verbose_name='論理削除')),
                ('check_duplicate', models.SmallIntegerField(default=0, verbose_name='重複チェック')),
                ('terminated_at', models.CharField(default='', max_length=16, verbose_name='契約解除日')),
            ],
            options={
                'verbose_name': 'コンテンツ',
                'verbose_name_plural': 'コンテンツ',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='cmsuser',
            unique_together=set([('acc_type_id', 'user_id')]),
        ),
    ]
