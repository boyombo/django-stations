# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-28 05:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heathen', '0003_auto_20161128_0519'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='industry',
            options={'ordering': ['name'], 'verbose_name_plural': 'Industries'},
        ),
    ]