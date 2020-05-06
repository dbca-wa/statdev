# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-01-14 09:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approvals', '0002_auto_20191210_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approval',
            name='status',
            field=models.IntegerField(choices=[(1, 'Current'), (2, 'Expired'), (3, 'Cancelled'), (4, 'Surrendered'), (5, 'Suspended'), (6, 'Reinstate'), (7, 'Pending')]),
        ),
    ]