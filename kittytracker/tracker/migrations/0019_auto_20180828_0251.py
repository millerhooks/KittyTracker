# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-08-28 07:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0018_merge_20180828_0251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
    ]
