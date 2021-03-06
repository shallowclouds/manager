# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-18 03:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fluData', '0011_auto_20171115_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='change_time',
            field=models.DateTimeField(blank=True, default='2017-11-18 03:40:11.171053+00:00', null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='all_things',
            field=models.TextField(blank=True, default='', null=True, verbose_name='搜索信息'),
        ),
        migrations.AlterField(
            model_name='house',
            name='community',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='社区'),
        ),
        migrations.AlterField(
            model_name='house',
            name='decor',
            field=models.CharField(blank=True, choices=[('清水', '清水'), ('简装', '简装'), ('中装', '中装'), ('精装', '精装'), ('豪装', '豪装')], default='', max_length=50, null=True, verbose_name='装修情况'),
        ),
        migrations.AlterField(
            model_name='house',
            name='house_type',
            field=models.CharField(blank=True, choices=[('出售', 'SELL'), ('出租', 'RENT')], default='出售', max_length=20, null=True, verbose_name='类型'),
        ),
        migrations.AlterField(
            model_name='house',
            name='ikeys',
            field=models.CharField(blank=True, default='', max_length=40, null=True, verbose_name='钥匙位置'),
        ),
        migrations.AlterField(
            model_name='house',
            name='kind',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='户型'),
        ),
        migrations.AlterField(
            model_name='house',
            name='more',
            field=models.CharField(blank=True, default='', max_length=1000, null=True, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='house',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='客户姓名'),
        ),
        migrations.AlterField(
            model_name='house',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='手机号码'),
        ),
        migrations.AlterField(
            model_name='house',
            name='position',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='地址'),
        ),
        migrations.AlterField(
            model_name='house',
            name='price_unit',
            field=models.CharField(blank=True, choices=[('万元', '万元'), ('千元', '千元'), ('百元', '百元'), ('  元', '元')], default='W', max_length=20, null=True, verbose_name='售价单位'),
        ),
        migrations.AlterField(
            model_name='house',
            name='status',
            field=models.CharField(blank=True, choices=[('交易完成', '该交易已在本店完成'), ('失效', '该房源已失效（已出售或出租）'), ('有效', '该房源有效')], default='有效', max_length=20, null=True, verbose_name='资源状态'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(blank=True, max_length=20, verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='手机号码'),
        ),
    ]
