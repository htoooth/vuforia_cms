# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('identifier', models.CharField(unique=True, verbose_name='アカウントID', max_length=11)),
                ('user_id', models.IntegerField(null=True, verbose_name='ユーザーID')),
                ('acc_type_id', models.SmallIntegerField(verbose_name='アカウントタイプID', choices=[(1, 'Admin'), (2, 'Agency'), (3, 'Company')])),
                ('parent_admin_id', models.IntegerField(default=1, verbose_name='親AdminID')),
                ('parent_agency_id', models.IntegerField(default=0, verbose_name='親AgencyID')),
                ('user_running', models.SmallIntegerField(default=0, verbose_name='稼働フラグ')),
                ('enterprise', models.CharField(verbose_name='企業名', max_length=64)),
                ('person', models.CharField(verbose_name='担当者名', max_length=64)),
                ('address', models.CharField(verbose_name='住所', max_length=64)),
                ('email', models.EmailField(verbose_name='メールアドレス', max_length=75)),
                ('phone_number', models.CharField(verbose_name='電話番号', max_length=16)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 19, 20, 7, 59, 980452), editable=False, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(null=True, editable=False, verbose_name='更新日')),
            ],
            options={
                'verbose_name_plural': 'ユーザー',
                'verbose_name': 'ユーザー',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('user_profile_id', models.IntegerField(unique=True, verbose_name='AdminID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AgencyUser',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('user_profile_id', models.IntegerField(unique=True, verbose_name='AgencyID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyUser',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('user_profile_id', models.IntegerField(unique=True, verbose_name='CompanyID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('contract_no', models.PositiveIntegerField(primary_key=True, serialize=False, verbose_name='契約番号')),
                ('title', models.CharField(verbose_name='タイトル', max_length=64)),
                ('target_id', models.CharField(verbose_name='ターゲットID', max_length=128)),
                ('mapping_url', models.CharField(verbose_name='マッピングURL', max_length=128)),
                ('open_from', models.CharField(verbose_name='公開期間 自', max_length=16)),
                ('open_to', models.CharField(null=True, verbose_name='公開期間 至', max_length=16)),
                ('is_open', models.SmallIntegerField(default=0, verbose_name='公開フラグ')),
                ('sort', models.IntegerField(default=0, verbose_name='ソートインデックス')),
                ('user_id', models.IntegerField(verbose_name='CompanyID')),
                ('recognition', models.SmallIntegerField(default=0, verbose_name='認識率')),
                ('contracted_at', models.CharField(verbose_name='契約日', max_length=16)),
                ('delete_flag', models.SmallIntegerField(default=1, verbose_name='論理削除')),
                ('check_duplicate', models.SmallIntegerField(default=0, verbose_name='重複チェック')),
                ('terminated_at', models.CharField(default='', verbose_name='契約解除日', max_length=16)),
            ],
            options={
                'verbose_name_plural': 'コンテンツ',
                'verbose_name': 'コンテンツ',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='userprofile',
            unique_together=set([('acc_type_id', 'user_id')]),
        ),
    ]
