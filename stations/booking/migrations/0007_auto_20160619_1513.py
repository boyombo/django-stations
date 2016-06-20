# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-19 15:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='code',
        ),
        migrations.AddField(
            model_name='token',
            name='uuid',
            field=models.CharField(max_length=100, null=True),
        ),
    ]