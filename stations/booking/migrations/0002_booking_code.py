# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-18 16:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='code',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
