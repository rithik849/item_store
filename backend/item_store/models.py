import datetime
from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator 
from products.models import Product
from django.contrib.auth.models import AbstractUser, AbstractBaseUser

# Create your models here.


class Customer(AbstractUser):

    username = models.TextField(max_length=50,unique=True)
    email = models.EmailField(max_length=100)
    
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.username + " " + self.email
    
class Review(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment = models.TextField()
    
class Basket(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    


    

# class Item(models.Model):
    
#     name 
#     price 
#     item_type
#     quantity
    
# class Orders(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     product = models.ManyToOneRel
#     quantity = models.IntegerField
#     date = models.DateField()
    