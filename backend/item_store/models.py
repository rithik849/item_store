import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from products.models import Product
from django.contrib.auth.models import AbstractUser
from decimal import Decimal

# Create your models here.


class Customer(AbstractUser):

    username = models.TextField(max_length=50,unique=True, blank=False)
    email = models.EmailField(max_length=100, unique = True, blank = False)
    password = models.TextField(max_length=255)
    total_basket_cost = models.DecimalField(default=Decimal(0), max_digits=30,decimal_places=2)
    
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"{self.username} {self.email}"
    
    def save(self,**kwargs):
        customer_id = self.id # type: ignore
        items = Basket.objects.filter(customer__id = customer_id)
        cost = 0
        for item in items:
            cost += item.product.price * item.quantity
        self.total_basket_cost = Decimal(str(cost))
        super().save(**kwargs)
    
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
    
    def save(self,**kwargs):
        super().save(**kwargs)
        self.customer.save()

    def delete(self,**kwargs):
        super().delete(**kwargs)
        self.customer.save()
    
class OrderNumber(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.datetime.today)
    total_cost = models.DecimalField(default=Decimal(0), max_digits=30, decimal_places=2)
    
    def __str__(self):
        return f"{self.id} {self.date}" # type: ignore
    
    def save(self,**kwargs):
        order_number_id = self.id # type: ignore
        orders = Order.objects.filter(order_number__id = self.id) # type: ignore
        cost = 0
        for order in orders:
            cost += order.product.price * order.quantity
        self.total_cost = Decimal(str(cost))
        super().save(**kwargs)
    
class Order(models.Model):
    order_number = models.ForeignKey(OrderNumber, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ('order_number','product')
    
    def __str__(self):
        return f"{self.order_number} {self.product} {self.quantity}"
    
    def save(self,**kwargs):
        super().save(**kwargs)
        self.order_number.save() # type: ignore
    

    


    

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
    