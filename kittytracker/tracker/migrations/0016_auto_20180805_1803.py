# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-08-05 23:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0015_auto_20180805_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat',
            name='birthday',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]