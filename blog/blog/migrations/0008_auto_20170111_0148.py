# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-11 01:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20170110_0849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='last_modified_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='修改时间'),
        ),
    ]
