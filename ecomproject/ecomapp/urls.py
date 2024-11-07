from django.urls import path, include
from . import views

urlpatterns = [
    path('sellerlogin/', views.sellerlogin),
    path('customerlogin/', views.customerlogin),
    path('sellerregister/', views.sellerregister),
    path('customerregister/', views.customerregister),
    path('createproduct/', views.createproduct),
    path('getproducts/', views.getproducts),
    path('hello/', views.hello),
    path('getsellerproducts/', views.getproductsofseller),
    path('order/', views.order),
    path('fetchorders/', views.fetchorder),
    path('fetchordersforseller/', views.fetchorderforseller),
    path('updatecustomer/', views.updatecustomer)
]