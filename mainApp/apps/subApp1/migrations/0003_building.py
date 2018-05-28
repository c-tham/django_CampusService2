# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-28 05:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subApp1', '0002_auto_20180528_0238'),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buildingName', models.CharField(max_length=255)),
                ('officeRoom', models.CharField(max_length=255)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('personID_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='personIDBuilding', to='subApp1.Person')),
            ],
        ),
    ]