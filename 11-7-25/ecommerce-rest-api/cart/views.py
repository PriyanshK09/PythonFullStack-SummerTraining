from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Cart, UserProduct
from .serializers import CartSerializer, AddToCartSerializer, UpdateCartSerializer
from .decorators import inventory_check
from products.models import Product

class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@inventory_check
def add_to_cart(request):
    serializer = AddToCartSerializer(data=request.data)
    if serializer.is_valid():
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id)
        
        cart_item, created = UserProduct.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return Response({
            'message': 'Product added to cart successfully',
            'cart': CartSerializer(cart).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, item_id):
    serializer = UpdateCartSerializer(data=request.data)
    if serializer.is_valid():
        quantity = serializer.validated_data['quantity']
        
        cart_item = get_object_or_404(
            UserProduct, 
            id=item_id, 
            cart__user=request.user
        )
        
        # Check inventory
        if cart_item.product.stock_quantity < quantity:
            return Response({
                'error': f'Insufficient stock. Only {cart_item.product.stock_quantity} items available.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return Response({
            'message': 'Cart updated successfully',
            'cart': CartSerializer(cart_item.cart).data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(
        UserProduct, 
        id=item_id, 
        cart__user=request.user
    )
    
    cart = cart_item.cart
    cart_item.delete()
    
    return Response({
        'message': 'Item removed from cart successfully',
        'cart': CartSerializer(cart).data
    })

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.cart_items.all().delete()
    
    return Response({
        'message': 'Cart cleared successfully',
        'cart': CartSerializer(cart).data
    })

# Web views for cart pages
@login_required
def cart_page(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {
        'cart': cart,
        'cart_items': cart.cart_items.all(),
    }
    return render(request, 'cart/cart.html', context)

@login_required
@require_POST
def add_to_cart_web(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    
    product = get_object_or_404(Product, id=product_id)
    
    # Check inventory
    if product.stock_quantity < quantity:
        messages.error(request, f'Insufficient stock. Only {product.stock_quantity} items available.')
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = UserProduct.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        if cart_item.quantity > product.stock_quantity:
            cart_item.quantity = product.stock_quantity
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart successfully!')
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def update_cart_web(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(UserProduct, id=item_id, cart__user=request.user)
        
        if cart_item.product.stock_quantity < quantity:
            messages.error(request, f'Insufficient stock. Only {cart_item.product.stock_quantity} items available.')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully!')
    
    return redirect('cart-page')

@login_required
def remove_from_cart_web(request, item_id):
    cart_item = get_object_or_404(UserProduct, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} removed from cart.')
    return redirect('cart-page')

@login_required
def clear_cart_web(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.cart_items.all().delete()
    messages.success(request, 'Cart cleared successfully!')
    return redirect('cart-page')