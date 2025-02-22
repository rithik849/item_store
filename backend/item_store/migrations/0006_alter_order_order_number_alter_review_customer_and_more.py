# Generated by Django 4.2.11 on 2024-06-11 16:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('item_store', '0005_remove_order_customer_remove_order_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='item_store.ordernumber'),
        ),
        migrations.AlterField(
            model_name='review',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='review',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('customer', 'product')},
        ),
    ]
