# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-09 10:12
from __future__ import unicode_literals

from django.db import migrations


def move_uuid(apps, schema_editor):
    Pharmacy = apps.get_model("drugshare", "Pharmacy")
    Device = apps.get_model("drugshare", "Device")
    for pharmacy in Pharmacy.objects.all():
        Device.objects.create(uuid=pharmacy.uuid, pharmacy=pharmacy)


class Migration(migrations.Migration):

    dependencies = [
        ('drugshare', '0020_device'),
    ]

    operations = [
        migrations.RunPython(move_uuid),
    ]
