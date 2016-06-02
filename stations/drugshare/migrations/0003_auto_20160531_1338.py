# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-31 13:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drugshare', '0002_auto_20160530_2021'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('expiry_date', models.DateField()),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='pharmacy',
            options={'verbose_name_plural': 'Pharmacies'},
        ),
        migrations.AddField(
            model_name='drug',
            name='pharmacy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drugshare.Pharmacy'),
        ),
    ]