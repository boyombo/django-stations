# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-14 05:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parcel', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='gender',
        ),
    ]