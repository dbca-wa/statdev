# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-14 08:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0042_auto_20171110_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='status',
            field=models.IntegerField(choices=[(1, 'Referred'), (2, 'Responded'), (3, 'Recalled'), (4, 'Expired'), (5, 'With Admin')], default=5),
        ),
    ]
