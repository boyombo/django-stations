# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-20 09:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0011_auto_20160620_0937'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estate',
            name='email',
        ),
    ]
