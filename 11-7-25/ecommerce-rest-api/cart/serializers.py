from rest_framework import serializers
from .models import Cart, UserProduct
from products.serializers import ProductSerializer

class UserProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = UserProduct
        fields = ['id', 'product', 'quantity', 'subtotal', 'added_at']

class CartSerializer(serializers.ModelSerializer):
    cart_items = UserProductSerializer(many=True, read_only=True)
    total_amount = serializers.ReadOnlyField()
    total_items = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'cart_items', 'total_amount', 'total_items', 'created_at', 'updated_at']

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)

class UpdateCartSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)