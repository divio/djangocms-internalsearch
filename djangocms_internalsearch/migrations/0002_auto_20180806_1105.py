# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-06 10:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_internalsearch', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='created_on',
            field=models.DateTimeField(),
        ),
    ]
