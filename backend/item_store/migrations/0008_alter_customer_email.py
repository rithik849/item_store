# Generated by Django 4.2.13 on 2024-06-18 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item_store', '0007_alter_basket_customer_alter_basket_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
    ]
