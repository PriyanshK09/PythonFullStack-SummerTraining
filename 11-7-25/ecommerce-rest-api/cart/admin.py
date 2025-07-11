from django.contrib import admin
from .models import Cart, UserProduct

class UserProductInline(admin.TabularInline):
    model = UserProduct
    extra = 0
    readonly_fields = ('subtotal', 'added_at')
    fields = ('product', 'quantity', 'subtotal', 'added_at')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_items', 'total_amount', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    ordering = ('-updated_at',)
    readonly_fields = ('total_items', 'total_amount', 'created_at', 'updated_at')
    inlines = [UserProductInline]
    
    fieldsets = (
        (None, {
            'fields': ('user',)
        }),
        ('Cart Summary', {
            'fields': ('total_items', 'total_amount'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(UserProduct)
class UserProductAdmin(admin.ModelAdmin):
    list_display = ('cart_user', 'product', 'quantity', 'subtotal', 'added_at')
    list_filter = ('added_at', 'product__category')
    search_fields = ('cart__user__username', 'product__name')
    ordering = ('-added_at',)
    readonly_fields = ('subtotal', 'added_at')
    
    def cart_user(self, obj):
        return obj.cart.user.username
    cart_user.short_description = 'User'
    cart_user.admin_order_field = 'cart__user__username'