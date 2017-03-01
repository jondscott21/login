# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 04:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logReg', '0006_remove_travel_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travel',
            name='plan',
        ),
        migrations.AddField(
            model_name='travel',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='travel', to='logReg.User'),
        ),
    ]