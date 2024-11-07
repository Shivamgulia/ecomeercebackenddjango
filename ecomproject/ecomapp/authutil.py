import os
from dotenv import load_dotenv
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from .models import *

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = 'HS256'  

def authenticateCustomer(bearer_token):

    if not bearer_token.startswith("Bearer "):
        print("Invalid token format. Expected 'Bearer {token}'.")
        return None

    token = bearer_token.split(" ")[1]
    
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


        user = Customer.objects.filter(id=payload['user_id']).first()

        userdto = {'name':user.name, 'email':user.email, 'address':user.address, 'contact':user.contact, 'id': user.id}
        return userdto

    except ExpiredSignatureError:
        print("Token has expired.")
        return None
    except InvalidTokenError:
        print("Invalid token.")
        return None



def authenticateSeller(bearer_token):

    if not bearer_token.startswith("Bearer "):
        print("Invalid token format. Expected 'Bearer {token}'.")
        return None

    token = bearer_token.split(" ")[1]
    
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


        user = Seller.objects.filter(id=payload['user_id']).first()

        userdto = {'name':user.name, 'email':user.email, 'address':user.address, 'contact':user.contact, 'id': user.id}
        return userdto

    except ExpiredSignatureError:
        print("Token has expired.")
        return None
    except InvalidTokenError:
        print("Invalid token.")
        return None