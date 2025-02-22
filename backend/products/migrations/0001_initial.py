# Generated by Django 4.2.13 on 2024-06-27 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('type', models.CharField(max_length=30)),
                ('price', models.FloatField()),
                ('stock', models.PositiveSmallIntegerField()),
            ],
        ),
    ]
