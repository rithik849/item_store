from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from item_store.models import Customer, Order, OrderNumber, Review, Basket

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass
    
@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderNumber)
class OrderNumberAdmin(admin.ModelAdmin):
    pass