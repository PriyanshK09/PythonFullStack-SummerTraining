from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='crud/logout.html'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('stock/<str:ticker>/', views.stock_detail, name='stock_detail'),
    path('buy/<str:ticker>/', views.buy_stock, name='buy_stock'),
    path('search/', views.search_stocks, name='search_stocks'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('watchlist/add/<str:ticker>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('wallet/', views.wallet, name='wallet'),
    path('add-money/', views.add_money, name='add_money'),
]