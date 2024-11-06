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
# from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, permission_classes
from .serializer import *
from rest_framework.permissions import AllowAny

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
        return Response(
            {"detail": "Seller Created"},
            status=status.HTTP_201_CREATED
        )
    return Response(
        {"detail": "Request Failed"},
        status=status.HTTP_400_BAD_REQUEST
    )
