from django.urls import path
from . import views

urlpatterns = [
    # API endpoints
    path('register/', views.register, name='register'),
    path('login/', views.login_api, name='login'),
    path('logout/', views.logout_api, name='logout'),
    
    # Web pages
    path('signup/', views.register_page, name='signup'),
    path('signin/', views.login_page, name='signin'),
    path('signout/', views.logout_page, name='signout'),
    path('profile/', views.profile_page, name='profile'),
]