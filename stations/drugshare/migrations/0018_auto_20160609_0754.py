# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-09 07:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugshare', '0017_outlet_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drug',
            name='pack_size',
            field=models.IntegerField(default=1),
        ),
    ]
