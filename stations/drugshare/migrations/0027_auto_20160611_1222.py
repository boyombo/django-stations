# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-11 12:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drugshare', '0026_token'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='token',
            unique_together=set([('code', 'when')]),
        ),
    ]
