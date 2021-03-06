# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-13 02:06
from __future__ import unicode_literals

import os

from django.db import migrations
from django.core.management import call_command

fixture_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../fixtures'))


def load_fixture(apps, schema_editor):
    print(fixture_dir)
    call_command('loaddata', os.path.join(fixture_dir, 'countries.json'))


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0003_remove_useraddress_profile_address'),
    ]

    operations = [
        migrations.RunPython(load_fixture)
    ]
