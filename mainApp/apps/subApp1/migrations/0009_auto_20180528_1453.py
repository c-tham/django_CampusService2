# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-28 14:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subApp1', '0008_auto_20180528_0703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mealgroup',
            name='ID_mealType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mealTypeID', to='subApp1.MealCardType'),
        ),
    ]
