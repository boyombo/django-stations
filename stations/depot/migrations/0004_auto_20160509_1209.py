# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-09 12:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('depot', '0003_auto_20160509_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='fuel_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='num_cars',
            field=models.PositiveIntegerField(choices=[(0, '1 - 10'), (1, '11 - 20'), (2, '> 20')]),
        ),
    ]
