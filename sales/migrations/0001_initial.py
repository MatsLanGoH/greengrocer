# Generated by Django 2.0 on 2017-12-12 03:36

from django.db import migrations, models
import django.db.models.deletion


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
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_items', models.PositiveIntegerField(help_text='個数を記入してください')),
                ('amount', models.PositiveIntegerField(help_text='売り上げ金額を記入してください')),
                ('created_at', models.DateTimeField(blank=True, help_text='販売日時を入力してください', null=True)),
                ('fruit', models.ForeignKey(help_text='果物を指定してください', on_delete=django.db.models.deletion.CASCADE, to='sales.Fruit')),
            ],
        ),
    ]
