# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-28 02:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subApp1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='userGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('person_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='personIDFrom', to='subApp1.Person')),
            ],
        ),
        migrations.CreateModel(
            name='userType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameType', models.CharField(max_length=255)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='usergroup',
            name='userType_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userTypeFrom', to='subApp1.userType'),
        ),
    ]
