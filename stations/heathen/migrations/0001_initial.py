# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-20 16:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('birthday', models.DateField()),
                ('availability', models.PositiveIntegerField(choices=[(0, 'Unavailable'), (1, 'Available')])),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heathen.Location')),
            ],
        ),
    ]
