# Generated by Django 2.0 on 2017-12-21 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0007_auto_20171221_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fruit',
            name='name',
            field=models.CharField(help_text='果物の名称を記入してください', max_length=100, unique=True),
        ),
    ]