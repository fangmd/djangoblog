# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-25 04:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_quanzhifashi'),
    ]

    operations = [
        migrations.AddField(
            model_name='quanzhifashi',
            name='body',
            field=models.TextField(default=' NULL', verbose_name='正文'),
        ),
    ]
