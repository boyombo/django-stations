# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-02 16:43
from __future__ import unicode_literals

from django.db import migrations


def move_messages(apps, schema_editor):
    Message = apps.get_model('medic', 'Message')
    Request = apps.get_model('medic', 'BloodRequest')
    for req in Request.objects.all():
        Message.objects.create(
            text=req.comment,
            request=req,
            subscriber=req.subscriber,
            when=req.when)


class Migration(migrations.Migration):

    dependencies = [
        ('medic', '0003_message'),
    ]

    operations = [
        migrations.RunPython(move_messages),
    ]