# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-14 05:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0022_auto_20170314_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vessel',
            name='engine',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vessel',
            name='passenger_capacity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vessel',
            name='registration',
            field=models.ManyToManyField(blank=True, to='applications.Document'),
        ),
        migrations.AlterField(
            model_name='vessel',
            name='size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vessel',
            name='vessel_id',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='vessel',
            name='vessel_type',
            field=models.SmallIntegerField(blank=True, choices=[(0, 'Vessel'), (1, 'Craft')], null=True),
        ),
    ]