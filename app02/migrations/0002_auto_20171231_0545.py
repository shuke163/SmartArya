# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-31 05:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app02', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostinfo',
            name='business',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='app02.BusiNess', verbose_name='所属业务线'),
        ),
    ]
