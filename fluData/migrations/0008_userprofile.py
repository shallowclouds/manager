# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-04 09:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fluData', '0007_auto_20171007_1841'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('name', models.CharField(max_length=20, verbose_name='姓名')),
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=3, verbose_name='用户等级')),
                ('phone', models.CharField(max_length=20, null=True, verbose_name='手机号码')),
                ('lastCheck', models.DateField(blank=True, null=True, verbose_name='上次签到时间')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
