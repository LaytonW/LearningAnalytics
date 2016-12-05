# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-05 09:16
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presentation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='average',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='grades',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), null=True, size=None),
        ),
        migrations.AddField(
            model_name='student',
            name='risk',
            field=models.FloatField(null=True),
        ),
    ]
