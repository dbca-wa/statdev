# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-21 02:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0023_auto_20170815_1700'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganisationContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=128, verbose_name='Given name(s)')),
                ('last_name', models.CharField(blank=True, max_length=128)),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=50, null=True)),
                ('fax_number', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
