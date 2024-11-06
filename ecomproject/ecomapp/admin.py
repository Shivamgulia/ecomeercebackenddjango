from django.contrib import admin
from .models import *
# Register your models here.
admin.register([Seller, CartItems,Carts, Customer, Orders, Product])
