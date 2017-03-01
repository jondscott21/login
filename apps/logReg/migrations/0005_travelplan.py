# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-25 06:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logReg', '0004_travel_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='TravelPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('the_travel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logReg.Travel')),
                ('the_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logReg.User')),
            ],
        ),
    ]
