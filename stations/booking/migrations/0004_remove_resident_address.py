# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-19 10:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_estate_resident'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resident',
            name='address',
        ),
    ]