# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-11 08:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('applications', '0033_organisationpending_submit_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisationpending',
            name='assignee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='org_pending_assignee', to=settings.AUTH_USER_MODEL),
        ),
    ]
