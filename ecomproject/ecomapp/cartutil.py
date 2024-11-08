from .models import *


def deleteitemsfromcart(user, product_id):
    try:
        # Get the customer's active cart
        cart = Carts.objects.get(buyer=user['id'])
    except Carts.DoesNotExist:
        return True
    
    cart_items = CartItems.objects.filter(cart=cart, product__id=product_id)
    
    if not cart_items.exists():
        return False
    
    deleted_count, _ = cart_items.delete()
    return True