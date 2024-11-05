from rest_framework import serializers
from .models import Customer, Seller, Product, Orders, CartItems, Carts  

class CustomerSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Customer  
        fields = '__all__'  

class SellerSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Seller  
        fields = '__all__'  

class ProductSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Product  
        fields = '__all__'  

class OrdersSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Orders  
        fields = '__all__'  

class CartItemsSerializer(serializers.ModelSerializer): 
    class Meta:
        model = CartItems  
        fields = '__all__'  

class CartsSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Carts  
        fields = '__all__'  
