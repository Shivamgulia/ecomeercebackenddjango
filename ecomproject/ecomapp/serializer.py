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

# class CartItemsSerializer(serializers.ModelSerializer): 
#     class Meta:
#         model = CartItems  
#         fields = '__all__'  

class CartsSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Carts  
        fields = '__all__'  

class CartItemSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.FloatField(source='product.price', read_only=True)
    product_discounted_price = serializers.FloatField(source='product.discounted_price', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItems
        fields = ['product', 'product_name', 'product_price', 'product_discounted_price', 'quantity', 'total_price','product_image']

    def get_total_price(self, obj):
        return obj.quantity * obj.product.discounted_price

    def get_product_image(self, obj):

        return obj.product.image