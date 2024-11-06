from django.urls import path, include
from . import views

urlpatterns = [
    path('sellerlogin/', views.sellerlogin),
    path('customerlogin/', views.customerlogin),
    path('sellerregister/', views.sellerregister),
    path('customerregister/', views.customerregister)
]