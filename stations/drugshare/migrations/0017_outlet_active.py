# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-08 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugshare', '0016_auto_20160607_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='outlet',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]