# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-06 23:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('depot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='current_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
