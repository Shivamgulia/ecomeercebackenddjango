from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import *
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view, permission_classes
from .serializer import *
from rest_framework.permissions import AllowAny
from .authutil import *
from django.forms.models import model_to_dict

@api_view(['POST'])
@permission_classes([AllowAny])
def sellerlogin(request):
    print(request.data)
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = None
    existsInSeller = Seller.objects.filter(name=username).exists()
    if existsInSeller : 
        user = Seller.objects.filter(name=username).first()
        print(user)
        is_password_correct = check_password(password, user.password)
        # is_password_correct = password ==  user.password
        if is_password_correct:
            userdto = {'name':user.name, 'email':user.email, 'address':user.address, 'contact':user.contact, 'id':user.id}
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': userdto
            },  status=status.HTTP_206_PARTIAL_CONTENT)
        else :
            return Response(
                {"detail": "Auth Failed"},
                status=status.HTTP_401_UNAUTHORIZED
            )

    else:
        return Response(
            {"detail": "No user found"},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def customerlogin(request):
    print(request.data)
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = None
    existsInCustomer = Customer.objects.filter(name=username).exists()
    if existsInCustomer : 
        user = Customer.objects.filter(name=username).first()
        print(user)
        is_password_correct = check_password(password, user.password)

        if is_password_correct:
            userdto = {'name':user.name, 'email':user.email, 'address':user.address, 'contact':user.contact,'id':user.id}
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': userdto
            },  status=status.HTTP_206_PARTIAL_CONTENT)
        else :
            return Response(
                {"detail": "Auth Failed"},
                status=status.HTTP_401_UNAUTHORIZED
            )

    else:
        return Response(
            {"detail": "No user found"},
            status=status.HTTP_401_UNAUTHORIZED
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def sellerregister(request):
    print(request.data)
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    address = request.data.get('address')
    contact = request.data.get('contact')

    hashed_pass = make_password(password)
    new_user = {'name': username, 'password': hashed_pass, 'email': email, 'address': address, 'contact': contact}
    ser = SellerSerializer(data = new_user)
    if ser.is_valid():
        ser.save()
        return Response(
            {"detail": "Seller Created"},
            status=status.HTTP_201_CREATED
        )
    return Response(
        {"detail": "Request Failed"},
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['POST'])
@permission_classes([AllowAny])
def customerregister(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    address = request.data.get('address')
    contact = request.data.get('contact')

    hashed_pass = make_password(password)
    new_user = {'name': username, 'password': hashed_pass, 'email': email, 'address': address, 'contact': contact}
    ser = CustomerSerializer(data = new_user)
    if ser.is_valid():
        ser.save()
        new_user = Customer.objects.filter(name = username).first()
        new_cart = {"buyer" : new_user.id}
        ser_cart = CartsSerializer(data = new_cart)
        if ser_cart.is_valid():
            ser_cart.save()
        return Response(
            {"detail": "Customer Created"},
            status=status.HTTP_201_CREATED
        )
    return Response(
        {"detail": "Request Failed"},
        status=status.HTTP_400_BAD_REQUEST
    )



@api_view(['POST'])
@permission_classes([AllowAny])
def createproduct(request):
    name = request.data.get('name')
    image = request.data.get('image')
    seller:int = request.data.get('seller')
    price:float = request.data.get('price')
    discounted_price:float = request.data.get('discounted_price')
    description = request.data.get('description')

    new_product = {'name': name, 'image': image, 'seller': seller, 'price': price, 'discounted_price': discounted_price, 'description':description}
    ser = ProductSerializer(data = new_product)
    if ser.is_valid():
        ser.save()
        return Response(
            {"detail": "Product Created"},
            status=status.HTTP_201_CREATED
        )
    return Response(
        {"detail": "Request Failed"},
        status=status.HTTP_400_BAD_REQUEST
    )

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def getproducts(request):
#     products = Product.objects.all()
#     serialized_products = ProductSerializer(products, many=True)
#     return Response(
#         {"products": serialized_products.data},
#         status=status.HTTP_200_OK
#     )

@api_view(['GET'])
@permission_classes([AllowAny])
def getproducts(request):
    try:
        limit = int(request.query_params.get('limit', 10)) 
        offset = int(request.query_params.get('offset', 0)) 
    except ValueError:
        return Response(
            {"error": "Invalid limit or offset parameter"},
            status=status.HTTP_400_BAD_REQUEST
        )

    products = Product.objects.all()
    paginated_products = products[offset:offset + limit]
    serialized_products = ProductSerializer(paginated_products, many=True)

    response_data = {
        "count": products.count(),
        "next": f"{request.build_absolute_uri()}?limit={limit}&offset={offset + limit}" if offset + limit < products.count() else None,
        "previous": f"{request.build_absolute_uri()}?limit={limit}&offset={max(offset - limit, 0)}" if offset > 0 else None,
        "products": serialized_products.data
    }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def getproductsofseller(request):
    token = request.headers.get('Authorization')
    user = authenticateSeller(token)
    if not user:
        return Response(
            {"detail": "Request Failed"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    seller_products = Product.objects.filter(seller=user['id'])
    return Response(
        {
            "user": user,
            "products": ProductSerializer(seller_products, many=True).data
        },
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([AllowAny])
def order(request):
    # Retrieve the token from headers and authenticate the user
    token = request.headers.get('Authorization')
    user = authenticateCustomer(token)

    # If user authentication fails, return an unauthorized response
    if not user:
        return Response(
            {"detail": "Request Failed"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Get product_id and buyer from the request data
    product_id = request.data.get('product_id')
    buyer = request.data.get('buyer')
    
    # Fetch the product from the database based on product_id
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {"detail": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Print product details for debugging
    print("Product details:", model_to_dict(product))

    # Prepare the data for the new order
    new_order = {
        'product_id': product_id,
        'buyer': buyer,
        'total_price': product.discounted_price,  # Access field with dot notation
        'seller': product.seller.id  # Use seller's ID (primary key) instead of the object
    }

    # Initialize the OrdersSerializer with the new order data
    ser = OrdersSerializer(data=new_order)

    # Check if the serialized data is valid
    if ser.is_valid():
        ser.save()
        return Response(
            {"detail": "Order Completed"},
            status=status.HTTP_201_CREATED
        )
    else:
        # Print and return serializer errors for debugging
        print("Serializer errors:", ser.errors)
        return Response(
            {"detail": "Request Failed", "errors": ser.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def fetchorder(request):
    token = request.headers.get('Authorization')
    user = authenticateCustomer(token)
    if not user:
        return Response(
            {"detail": "Request Failed"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    print(user)
    customer_orders = Orders.objects.filter(buyer=user['id'])
    return Response(
        {
            "user": user,
            "orders": OrdersSerializer(customer_orders, many=True).data
        },
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@permission_classes([AllowAny])
def fetchorderforseller(request):
    token = request.headers.get('Authorization')
    user = authenticateSeller(token)
    if not user:
        return Response(
            {"detail": "Request Failed"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    print(user)
    seller_orders = Orders.objects.filter(seller=user['id'])
    return Response(
        {
            "orders": OrdersSerializer(seller_orders, many=True).data
        },
        status=status.HTTP_200_OK
    )


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def updatecustomer(request):

#     token = request.headers.get('Authorization')
#     user = authenticateCustomer(token)

#     print("hello")
#     if not user:
#         return Response(
#         {"detail": "Request Failed"},
#         status=status.HTTP_401_UNAUTHORIZED
#         )
    
#     address = request.data.get('address')
#     updated_user = Customer.objects.filter(id = user['id'])
#     print(updated_user,"user", user['id'])
#     print("abc")
#     updated_user['address'] = address
#     print(updated_user['id'])
#     ser = CustomerSerializer(data = updated_user)
#     if ser.is_valid():
#         ser.update()
#         return Response(
#             {"detail": "Order Completed"},
#             status=status.HTTP_201_CREATED
#         )
    
#     return Response(
#         {"detail": "Request Failed"},
#         status=status.HTTP_400_BAD_REQUEST
#     )

@api_view(['POST'])
@permission_classes([AllowAny])
def updatecustomer(request):
    token = request.headers.get('Authorization')
    user = authenticateCustomer(token)
    
    if not user:
        return Response(
            {"detail": "Request Failed"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        customer = Customer.objects.get(id=user['id'])
    except Customer.DoesNotExist:
        return Response(
            {"detail": "Customer not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    address = request.data.get('address')
    customer.address = address

    ser = CustomerSerializer(instance=customer, data=request.data, partial=True)
    if ser.is_valid():
        ser.save()
        return Response(
            {"detail": "Customer updated successfully"},
            status=status.HTTP_200_OK
        )
    
    return Response(
        ser.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['POST'])
@permission_classes([AllowAny])
def updateseller(request):
    token = request.headers.get('Authorization')
    user = authenticateCustomer(token)
    
    if not user:
        return Response(
            {"detail": "Request Failed"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        seller = Seller.objects.get(id=user['id'])
    except Seller.DoesNotExist:
        return Response(
            {"detail": "Seller not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    address = request.data.get('address')
    seller.address = address

    ser = CustomerSerializer(instance=seller, data=request.data, partial=True)
    if ser.is_valid():
        ser.save()
        return Response(
            {"detail": "Seller updated successfully"},
            status=status.HTTP_200_OK
        )
    
    return Response(
        ser.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def hello(request):
    token = request.headers.get('Authorization')
    user = authenticateCustomer(token)
    sellerproducts = Product.objects.filter()
    if not user:
        return Response(
        {"detail": "Request Failed"},
        status=status.HTTP_401_UNAUTHORIZED
        )   

    return Response(
        {"user": user},
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([AllowAny])
def addtocart(request):
    token = request.headers.get('Authorization')
    user = authenticateCustomer(token)
    
    if not user:
        return Response(
            {"detail": "Unauthorized"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    product_list = request.data.get('products', [])
    
    if not product_list:
        return Response(
            {"detail": "Product list is empty or missing"},
            status=status.HTTP_400_BAD_REQUEST
        )

    cart = Carts.objects.filter(buyer=user['id']).first()
    
    cart_item_responses = []  

    for item in product_list:
        product_id = item.get('product_id')
        quantity = item.get('quantity', 1)
        image_url = item.get('image') 

        try:
            product = Product.objects.get(id=product_id)
           
            cart_item = CartItems.objects.create(cart=cart, product=product, quantity=quantity)
            
            cart_item_responses.append({
                "product_id": product.id,
                "name": product.name,
                "quantity": quantity,
                "image": image_url  
            })
        except Product.DoesNotExist:
            return Response(
                {"detail": f"Product with ID {product_id} does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

    return Response(
        {"detail": "Items added to cart successfully", "items": cart_item_responses},
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def getcartitems(request):
    
    token = request.headers.get('Authorization')
    user = authenticateCustomer(token) 
    if not user:
        return Response(
            {"detail": "Unauthorized request"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        # Get the user's cart
        cart = Carts.objects.get(buyer=user['id'])
        cart_items = CartItems.objects.filter(cart=cart)
        
        # Serialize the cart items
        serialized_cart_items = CartItemSerializer(cart_items, many=True)
        return Response(serialized_cart_items.data, status=status.HTTP_200_OK)
        
    except Carts.DoesNotExist:
        return Response(
            {"detail": "Cart not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
@api_view(['DELETE'])
@permission_classes([AllowAny])  # Ensure that only authenticated users can delete items
def deletecartitem(request, product_id):

    token = request.headers.get('Authorization')
    user = authenticateCustomer(token) 
    if not user:
        return Response(
            {"detail": "Unauthorized request"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    try:
        # Get the customer's active cart
        cart = Carts.objects.get(buyer=user['id'])
    except Carts.DoesNotExist:
        return Response(
            {"detail": "Cart not found for this user."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    cart_items = CartItems.objects.filter(cart=cart, product__id=product_id)
    
    if not cart_items.exists():
        return Response(
            {"detail": "Product not found in your cart."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Delete all matching CartItems
    deleted_count, _ = cart_items.delete()
    return Response(
        {"detail": f"{deleted_count} item(s) removed from your cart."},
        status=status.HTTP_200_OK
    )

@api_view(['DELETE'])
@permission_classes([AllowAny])  # Ensure that only authenticated users can delete items
def deleteproduct(request, pid):

    token = request.headers.get('Authorization')
    user = authenticateSeller(token) 
    if not user:
        return Response(
            {"detail": "Unauthorized request"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # product_to_be_deleted = Product.objects.filter(id=pid)
    
    try:
        product = Product.objects.get(id=pid)
        
        # Delete only the orders related to the product
        Orders.objects.filter(product_id=product).delete()
        
        # Now delete the product itself
        product.delete()
        
        return Response(
            {"detail": "Product and related orders deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
    
    except Product.DoesNotExist:
        return Response(
            {"detail": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"detail": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def updateproduct(request):
    token = request.headers.get('Authorization')
    user = authenticateSeller(token)
    
    if not user:
        return Response(
            {"detail": "Request Failed"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    product_id = request.data.get('product_id')
    discounted_price = request.data.get('discounted_price')
    
    product = Product.objects.get(id=product_id)
    
    product.discounted_price = discounted_price

    ser = ProductSerializer(instance=product, data=request.data, partial=True)
    if ser.is_valid():
        ser.save()
        return Response(
            {"detail": "Product updated successfully"},
            status=status.HTTP_200_OK
        )
    
    return Response(
        ser.errors,
        status=status.HTTP_400_BAD_REQUEST
    )