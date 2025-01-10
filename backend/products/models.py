from decimal import Decimal
from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=40)
    type = models.CharField(max_length=30)
    price = models.DecimalField(default=Decimal(0), max_digits=30,decimal_places=2)
    stock = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return str(self.name)