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
    path('addtocart/',views.addtocart),
    path('getcartitems/',views.getcartitems),
    path('deletecartitem/<int:product_id>/', views.deletecartitem, name='delete_cart_item'),
    path('fetchordersforseller/', views.fetchorderforseller),
    path('updatecustomer/', views.updatecustomer),
    path('updateseller/', views.updateseller),
    path('deleteproduct/<int:pid>/', views.deleteproduct, name='pid'),
    path('updateproduct/', views.updateproduct)
]