from django.urls import path
from . import views

urlpatterns = [
    # API endpoints
    path('', views.CartView.as_view(), name='cart-detail'),
    path('add/', views.add_to_cart, name='add-to-cart'),
    path('update/<int:item_id>/', views.update_cart_item, name='update-cart-item'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('clear/', views.clear_cart, name='clear-cart'),
    
    # Web pages
    path('view/', views.cart_page, name='cart-page'),
    path('add-web/', views.add_to_cart_web, name='add-to-cart-web'),
    path('update-web/<int:item_id>/', views.update_cart_web, name='update-cart-web'),
    path('remove-web/<int:item_id>/', views.remove_from_cart_web, name='remove-from-cart-web'),
    path('clear-web/', views.clear_cart_web, name='clear-cart-web'),
]