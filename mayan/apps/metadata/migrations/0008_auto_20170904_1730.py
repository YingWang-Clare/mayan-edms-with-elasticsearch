# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-04 17:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0007_auto_20150918_0800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentmetadata',
            name='value',
            field=models.TextField(blank=True, db_index=True, null=True, verbose_name='Value'),
        ),
    ]
