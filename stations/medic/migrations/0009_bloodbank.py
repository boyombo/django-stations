# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-02-06 06:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medic', '0008_subscriber_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodBank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.TextField(blank=True)),
                ('latitude', models.CharField(blank=True, max_length=50)),
                ('longitude', models.CharField(blank=True, max_length=50)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medic.Location')),
            ],
        ),
    ]