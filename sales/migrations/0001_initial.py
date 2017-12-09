# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-09 05:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fruit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text='果物の名称を記入してください', max_length=200, unique=True)),
                ('price', models.PositiveIntegerField(help_text='果物の単価を記入してください')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('modified_at', models.DateField(auto_now=True)),
            ],
        ),
    ]
