# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-19 09:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drugshare', '0028_requestfeedback'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='requestfeedback',
            options={'verbose_name_plural': 'Request Feedback'},
        ),
    ]