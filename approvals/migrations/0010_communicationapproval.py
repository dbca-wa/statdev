# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-12 03:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0039_auto_20171012_1146'),
        ('approvals', '0009_auto_20170815_1700'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunicationApproval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comms_to', models.CharField(blank=True, max_length=256, null=True)),
                ('comms_from', models.CharField(blank=True, max_length=256, null=True)),
                ('subject', models.CharField(blank=True, max_length=256, null=True)),
                ('comms_type', models.IntegerField(choices=[(0, 'None'), (1, 'Phone'), (2, 'Email'), (3, 'Mail'), (4, 'System')], default=0)),
                ('details', models.TextField(blank=True, null=True)),
                ('state', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='applications.Application')),
                ('records', models.ManyToManyField(blank=True, related_name='communication_approvals_docs', to='applications.Record')),
            ],
        ),
    ]
