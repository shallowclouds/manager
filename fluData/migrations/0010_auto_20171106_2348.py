# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-06 15:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fluData', '0009_house'),
    ]

    operations = [
        migrations.RenameField(
            model_name='house',
            old_name='keys',
            new_name='ikeys',
        ),
    ]
