# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-02-22 19:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jamb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='question',
        ),
        migrations.AddField(
            model_name='question',
            name='answer_A',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='question',
            name='answer_B',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='question',
            name='answer_C',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='question',
            name='answer_D',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='question',
            name='answer_E',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='question',
            name='correct',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], max_length=5, null=True),
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
    ]
