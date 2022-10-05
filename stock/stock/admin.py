from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['email', 'status', 'address', 'order_id_in_shop']
    list_filter = ['email', 'status', 'address']
    inlines = [
        OrderItemInline,
    ]
    filter_horizontal = ('book_inst',)
    search_fields = ['order_id_in_shop', 'email']
