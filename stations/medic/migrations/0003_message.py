# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-02 16:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('medic', '0002_bloodrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('when', models.DateTimeField(default=django.utils.timezone.now)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medic.BloodRequest')),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medic.Subscriber')),
            ],
        ),
    ]