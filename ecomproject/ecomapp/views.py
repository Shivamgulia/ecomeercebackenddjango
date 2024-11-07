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
            userdto = {'name':user.name, 'email':user.email, 'address':user.address, 'contact':user.contact}
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
            userdto = {'name':user.name, 'email':user.email, 'address':user.address, 'contact':user.contact}
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

    token = request.headers.get('Authorization')
    user = authenticateCustomer(token)

    if not user:
        return Response(
        {"detail": "Request Failed"},
        status=status.HTTP_401_UNAUTHORIZED
        )
    
    product_id = request.data.get('product_id')
    buyer:int = request.data.get('buyer')
    total_price = request.data.get('total_price')
    
    new_order = {'product_id': product_id, 'buyer': buyer, 'total_price' : total_price}
    ser = OrdersSerializer(data = new_order)
    if ser.is_valid():
        ser.save()
        return Response(
            {"detail": "Order Completed"},
            status=status.HTTP_201_CREATED
        )
    return Response(
        {"detail": "Request Failed"},
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
    # Retrieve token and authenticate user
    token = request.headers.get('Authorization')
    user = authenticateCustomer(token)
    
    # If user is not authenticated, return an unauthorized response
    if not user:
        return Response(
            {"detail": "Unauthorized"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Retrieve product list from request data
    product_list = request.data.get('products', [])
    
    if not product_list:
        return Response(
            {"detail": "Product list is empty or missing"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Get or create a cart for the authenticated user
    cart = Carts.objects.filter(buyer=user['id']).first()
    
    # Iterate through each item in the product list and add to cart items
    for item in product_list:
        product_id = item.get('product_id')
        quantity = item.get('quantity', 1)
        
        try:
            product = Product.objects.get(id=product_id)
            CartItems.objects.create(cart=cart, product=product, quantity=quantity)
        except Product.DoesNotExist:
            return Response(
                {"detail": f"Product with ID {product_id} does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

    return Response(
        {"detail": "Items added to cart successfully"},
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def getcartitems(request):
    # Retrieve the token from the headers and authenticate user
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

    

