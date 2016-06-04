# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-04 12:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugshare', '0012_auto_20160604_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='drug',
            name='brand_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='drug',
            name='pack_size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='drug',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Generic Name'),
        ),
    ]