from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from item_store.models import Customer

class CustomerAdmin(admin.ModelAdmin):
    fields = ['username','email','password']


admin.site.register(Customer,CustomerAdmin)