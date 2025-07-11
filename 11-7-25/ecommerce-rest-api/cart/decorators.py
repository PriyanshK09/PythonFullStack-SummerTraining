from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def inventory_check(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        try:
            from products.models import Product
            product = Product.objects.get(id=product_id)
            
            if product.stock_quantity < quantity:
                return Response({
                    'error': f'Insufficient stock. Only {product.stock_quantity} items available.'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            if not product.is_active:
                return Response({
                    'error': 'Product is not available.'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Product.DoesNotExist:
            return Response({
                'error': 'Product not found.'
            }, status=status.HTTP_404_NOT_FOUND)
            
        return func(self, request, *args, **kwargs)
    return wrapper