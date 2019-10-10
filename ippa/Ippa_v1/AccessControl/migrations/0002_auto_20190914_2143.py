# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-09-14 21:43
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AccessControl', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ippauser',
            name='achievements',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=[], null=True),
        ),
        migrations.AddField(
            model_name='ippauser',
            name='favourite_hands',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10), blank=True, default=[], null=True, size=None),
        ),
        migrations.AddField(
            model_name='ippauser',
            name='is_mobile_number_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ippauser',
            name='poa_image',
            field=models.TextField(blank=True, help_text='Proof of address.', null=True),
        ),
        migrations.AlterField(
            model_name='ippauser',
            name='kyc_status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Pending'), (0, 'Approved'), (2, 'Declined')], default=3),
        ),
        migrations.AlterField(
            model_name='ippauser',
            name='poi_image',
            field=models.TextField(blank=True, help_text='Proof of identity.(Kyc currently)', null=True),
        ),
    ]