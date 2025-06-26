from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Stock, UserStock, StockPriceHistory, Watchlist

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'username', 'first_name', 'last_name', 'balance', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'date_of_birth', 'profile_picture', 'balance')}),
    )

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['ticker', 'name', 'current_price', 'sector', 'exchange', 'last_updated']
    list_filter = ['sector', 'exchange', 'currency']
    search_fields = ['ticker', 'name']
    readonly_fields = ['last_updated', 'created_at']

@admin.register(UserStock)
class UserStockAdmin(admin.ModelAdmin):
    list_display = ['user', 'stock', 'transaction_type', 'quantity', 'buy_price', 'transaction_date']
    list_filter = ['transaction_type', 'transaction_date']
    search_fields = ['user__username', 'stock__ticker']

@admin.register(StockPriceHistory)
class StockPriceHistoryAdmin(admin.ModelAdmin):
    list_display = ['stock', 'price', 'volume', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['stock__ticker']

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'stock', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__username', 'stock__ticker']

admin.site.register(User, CustomUserAdmin)
