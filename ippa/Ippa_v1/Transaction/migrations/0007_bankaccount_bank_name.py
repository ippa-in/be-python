# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2020-05-06 19:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Transaction', '0006_remove_bankaccount_bank'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='bank_name',
            field=models.CharField(default='YES', max_length=255),
            preserve_default=False,
        ),
    ]