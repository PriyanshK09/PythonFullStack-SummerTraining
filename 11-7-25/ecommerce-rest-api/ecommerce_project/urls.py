from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

# Customize admin site
admin.site.site_header = "eCommerce Administration"
admin.site.site_title = "eCommerce Admin"
admin.site.index_title = "Welcome to eCommerce Administration"

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products_page, name='products-page'),
    path('category/<int:category_id>/', views.category_detail, name='category-detail-page'),
    path('api/', views.api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('cart/', include('cart.urls')),
    path('api/auth/', include('authentication.urls')),
    path('api/categories/', include('categories.urls')),
    path('api/products/', include('products.urls')),
    path('api/cart/', include('cart.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])