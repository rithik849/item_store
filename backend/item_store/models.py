import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from products.models import Product
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Customer(AbstractUser):

    username = models.TextField(max_length=50,unique=True)
    email = models.EmailField(max_length=100, unique = True)
    password = models.TextField(max_length=255)
    
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"{self.username} {self.email}"
    
class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment = models.TextField()
    
    class Meta:
        unique_together = ('customer','product')
    
    def __str__(self):
        return f"{self.customer} {self.product} {self.rating}"
    
class Basket(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ('customer','product')
    
    def __str__(self):
        return f"{self.customer} {self.product} {self.quantity}"
    
class OrderNumber(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.id} {self.date} {self.status}" # type: ignore
    
class Order(models.Model):
    order_number = models.ForeignKey(OrderNumber, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ('order_number','product')
    
    def __str__(self):
        return f"{self.order_number} {self.product} {self.quantity}"
    

    


    

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
    