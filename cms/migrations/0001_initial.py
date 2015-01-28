# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('identifier', models.CharField(unique=True, max_length=11, verbose_name='アカウントID')),
                ('user_id', models.IntegerField(null=True, verbose_name='ユーザーID')),
                ('acc_type_id', models.SmallIntegerField(choices=[(1, 'Admin'), (2, 'Agency'), (3, 'Company')], verbose_name='アカウントタイプID')),
                ('parent_admin_id', models.IntegerField(default=1, verbose_name='親AdminID')),
                ('parent_agency_id', models.IntegerField(null=True, verbose_name='親AgencyID')),
                ('user_running', models.SmallIntegerField(default=0, verbose_name='稼働フラグ')),
                ('enterprise', models.CharField(max_length=64, verbose_name='企業名')),
                ('person', models.CharField(max_length=64, verbose_name='担当者名')),
                ('address', models.CharField(max_length=64, verbose_name='住所')),
                ('email', models.EmailField(max_length=75, verbose_name='メールアドレス')),
                ('phone_number', models.CharField(max_length=16, verbose_name='電話番号')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 28, 19, 48, 13, 700056), editable=False, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(editable=False, null=True, verbose_name='更新日')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('user_profile_id', models.IntegerField(unique=True, null=True, verbose_name='AdminID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AgencyUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('user_profile_id', models.IntegerField(unique=True, null=True, verbose_name='AgencyID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('user_profile_id', models.IntegerField(unique=True, null=True, verbose_name='CompanyID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('contract_no', models.PositiveIntegerField(serialize=False, verbose_name='契約番号', primary_key=True)),
                ('title', models.CharField(max_length=64, verbose_name='タイトル')),
                ('target_id', models.CharField(max_length=128, verbose_name='ターゲットID')),
                ('mapping_url', models.CharField(max_length=128, verbose_name='マッピングURL')),
                ('open_from', models.CharField(max_length=16, verbose_name='公開期間 自')),
                ('open_to', models.CharField(max_length=16, null=True, verbose_name='公開期間 至')),
                ('is_open', models.SmallIntegerField(default=0, verbose_name='公開フラグ')),
                ('sort', models.IntegerField(default=0, verbose_name='ソートインデックス')),
                ('user_id', models.IntegerField(verbose_name='CompanyID')),
                ('recognition', models.SmallIntegerField(default=0, verbose_name='認識率')),
                ('contracted_at', models.CharField(max_length=16, verbose_name='契約日')),
                ('delete_flag', models.SmallIntegerField(default=1, verbose_name='論理削除')),
                ('check_duplicate', models.SmallIntegerField(default=0, verbose_name='重複チェック')),
                ('terminated_at', models.CharField(default='', max_length=16, verbose_name='契約解除日')),
                ('company', models.ForeignKey(verbose_name='Company', to=settings.AUTH_USER_MODEL)),
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
