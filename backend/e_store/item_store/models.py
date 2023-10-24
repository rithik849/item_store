from django.db import models
from django.urls import reverse

# Create your models here.


class Customer(models.Model):

    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Customer_detail", kwargs={"pk": self.pk})