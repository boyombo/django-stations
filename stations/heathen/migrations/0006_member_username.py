# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-29 10:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heathen', '0005_auto_20161128_0554'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='username',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
