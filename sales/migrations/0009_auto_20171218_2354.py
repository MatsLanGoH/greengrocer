# Generated by Django 2.0 on 2017-12-18 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0008_auto_20171218_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.PositiveIntegerField(blank=True, default=0, help_text='売り上げ金額を記入してください'),
        ),
    ]