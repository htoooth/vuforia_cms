# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('cms', '0016_auto_20150217_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(verbose_name='groups', related_query_name='user', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', related_name='user_set', to='auth.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_superuser',
            field=models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(verbose_name='user permissions', related_query_name='user', blank=True, help_text='Specific permissions for this user.', related_name='user_set', to='auth.Permission'),
            preserve_default=True,
        ),
    ]
