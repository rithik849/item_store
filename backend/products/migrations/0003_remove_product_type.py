# Generated by Django 5.1.2 on 2025-01-18 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='type',
        ),
    ]
