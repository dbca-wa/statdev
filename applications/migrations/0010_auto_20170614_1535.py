# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-14 07:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0009_auto_20170613_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communication',
            name='state',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]