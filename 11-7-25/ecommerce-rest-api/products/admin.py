from django.contrib import admin
from django.contrib import messages
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'is_in_stock', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at', 'price')
    search_fields = ('name', 'description', 'category__name')
    ordering = ('-created_at',)
    list_editable = ('price', 'stock_quantity', 'is_active')
    list_per_page = 25
    actions = ['mark_as_active', 'mark_as_inactive', 'add_stock']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock_quantity')
        }),
        ('Media & Status', {
            'fields': ('image', 'is_active')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'is_in_stock')
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:  # editing an existing object
            fieldsets = fieldsets + (
                ('Timestamps & Status', {
                    'fields': ('is_in_stock', 'created_at', 'updated_at'),
                    'classes': ('collapse',)
                }),
            )
        return fieldsets
    
    def is_in_stock(self, obj):
        return obj.is_in_stock
    is_in_stock.boolean = True
    is_in_stock.short_description = 'In Stock'
    
    # Custom admin actions
    def mark_as_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} products marked as active.', messages.SUCCESS)
    mark_as_active.short_description = "Mark selected products as active"
    
    def mark_as_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} products marked as inactive.', messages.SUCCESS)
    mark_as_inactive.short_description = "Mark selected products as inactive"
    
    def add_stock(self, request, queryset):
        # This would typically open a form to add stock, for now just add 10 to each
        for product in queryset:
            product.stock_quantity += 10
            product.save()
        self.message_user(request, f'Added 10 stock to {queryset.count()} products.', messages.SUCCESS)
    add_stock.short_description = "Add 10 stock to selected products"