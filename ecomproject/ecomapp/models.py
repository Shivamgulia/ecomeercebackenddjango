from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=50) 
    address = models.TextField()
    contact = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    password = models.TextField()

    def __str__(self):
        return self.name 

class Seller(models.Model):
    name = models.CharField(max_length=50)  
    address = models.TextField()  
    contact = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    password = models.TextField()

    def __str__(self):
        return self.name 

class Product(models.Model):
    name = models.CharField(max_length=50) 
    image = models.URLField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.name

class Orders(models.Model): 
    product_id = models.ForeignKey(Product)
    buyer = models.ForeignKey(Customer)
    total_price = models.FloatField()
        
    def __str__(self):
        return self.name

class Carts(models.Model):
    buyer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return "Cart"
    
class CartItems(models.Model):
    cart = models.ForeignKey(Carts)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()

    def __str__(self):
        return "Cart-Item"

