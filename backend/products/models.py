from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=40)
    type = models.CharField(max_length=30)
    price = models.FloatField()
    stock = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return str(self.name)