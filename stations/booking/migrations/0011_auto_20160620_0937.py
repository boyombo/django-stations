# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-20 09:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0010_auto_20160619_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='estate',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booked_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
