from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('<str:product_name>/', views.ProductDetailView.as_view(), name='product-detail'),
]