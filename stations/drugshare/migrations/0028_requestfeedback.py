# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-14 22:21
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drugshare', '0027_auto_20160611_1222'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_status', models.PositiveIntegerField(choices=[(0, 'Pending'), (1, 'Cancelled'), (2, 'Accepted'), (3, 'Done')])),
                ('message', models.TextField()),
                ('when', models.DateTimeField(default=datetime.datetime.now)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drugshare.DrugRequest')),
            ],
        ),
    ]
