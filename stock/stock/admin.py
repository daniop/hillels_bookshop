from django.contrib import admin

from .models import Order, OrderItem

#
# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     list_display = ['title', 'price', 'isbn']
#     list_filter = ['title', 'price', 'isbn']


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['email', 'status', 'address']
    list_filter = ['email', 'status', 'address']
    inlines = [
        OrderItemInline,
    ]
    filter_horizontal = ('book_inst',)
