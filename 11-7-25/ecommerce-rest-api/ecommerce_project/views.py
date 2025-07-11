from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.shortcuts import render
from products.models import Product
from categories.models import Category
from django.db.models import Q

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    """
    Welcome to the eCommerce REST API!
    This endpoint lists all available API endpoints.
    """
    return Response({
        'message': 'Welcome to eCommerce REST API',
        'version': '1.0',
        'endpoints': {
            'authentication': {
                'register': reverse('register', request=request, format=format),
                'login': reverse('login', request=request, format=format),
                'logout': reverse('logout', request=request, format=format),
            },
            'categories': {
                'list_categories': reverse('category-list', request=request, format=format),
                'category_detail': request.build_absolute_uri('/api/categories/{id}/'),
            },
            'products': {
                'list_products': reverse('product-list', request=request, format=format),
                'product_detail': request.build_absolute_uri('/api/products/{product-name}/'),
                'search_products': request.build_absolute_uri('/api/products/?search={query}'),
                'filter_by_category': request.build_absolute_uri('/api/products/?category={category_id}'),
                'filter_by_price': request.build_absolute_uri('/api/products/?price={price}'),
            },
            'cart': {
                'view_cart': reverse('cart-detail', request=request, format=format),
                'add_to_cart': reverse('add-to-cart', request=request, format=format),
                'update_cart_item': request.build_absolute_uri('/api/cart/update/{item_id}/'),
                'remove_from_cart': request.build_absolute_uri('/api/cart/remove/{item_id}/'),
                'clear_cart': reverse('clear-cart', request=request, format=format),
            },
            'admin_panel': request.build_absolute_uri('/admin/'),
        },
        'authentication': {
            'required': 'Token-based authentication required for most endpoints',
            'header_format': 'Authorization: Token {your_token}',
            'obtain_token': 'Use login endpoint to get authentication token'
        },
        'documentation': {
            'cart_functionality': 'Cart supports add, update, remove items with inventory checking',
            'user_types': 'customer (default), admin',
            'permissions': 'Most endpoints require authentication, some are read-only for anonymous users'
        }
    })

def home(request):
    """
    Home page view showing featured products and categories
    """
    # Get featured products (latest 8 products)
    featured_products = Product.objects.filter(is_active=True)[:8]
    
    # Get all active categories
    categories = Category.objects.filter(is_active=True)[:6]
    
    # Get latest products
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[:4]
    
    # Search functionality
    search_query = request.GET.get('search', '')
    search_results = []
    
    if search_query:
        search_results = Product.objects.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query),
            is_active=True
        )[:10]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'latest_products': latest_products,
        'search_query': search_query,
        'search_results': search_results,
    }
    
    return render(request, 'home.html', context)

def products_page(request):
    """
    Products listing page
    """
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query,
    }
    
    return render(request, 'products.html', context)

def category_detail(request, category_id):
    """
    Category detail page showing products in that category
    """
    category = Category.objects.get(id=category_id, is_active=True)
    products = Product.objects.filter(category=category, is_active=True)
    
    context = {
        'category': category,
        'products': products,
    }
    
    return render(request, 'category_detail.html', context)