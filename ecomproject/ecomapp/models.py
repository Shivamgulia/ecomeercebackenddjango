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
    image = models.TextField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.name

class Orders(models.Model): 
    product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    buyer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    total_price = models.FloatField()
    seller = models.ForeignKey(Seller, on_delete=models.DO_NOTHING)
        
    def __str__(self):
        return self.name

class Carts(models.Model):
    buyer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return "Cart"
    
class CartItems(models.Model):
    cart = models.ForeignKey(Carts, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()

    def __str__(self):
        return "Cart-Item"


