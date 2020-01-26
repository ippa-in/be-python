# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2020-01-23 19:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NotificationEngine', '0002_notification_mail'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('notification_str', models.CharField(max_length=255)),
                ('has_read', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]