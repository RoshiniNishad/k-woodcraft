from django.contrib import admin
from .models import Product , ContactMessage ,Cart, Payment


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'rating')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created_at')
    ordering = ('-created_at',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'created_at', 'total_price')
    search_fields = ('user__username', 'product__name')
    list_filter = ('created_at',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'product', 'location',
        'delivery_date', 'total_amount',
        'advance_payment', 'remaining_amount', 'created_at'
    )
    search_fields = ('user__username', 'product__name', 'location')
    list_filter = ('delivery_date', 'created_at')