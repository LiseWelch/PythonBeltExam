# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-10-18 16:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('belt_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appt',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='appts', to='belt_app.User'),
            preserve_default=False,
        ),
    ]
