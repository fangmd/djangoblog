# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-20 05:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20161119_1426'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Articale',
            new_name='Article',
        ),
    ]