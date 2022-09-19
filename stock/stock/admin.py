from django.contrib import admin

from .models import Book, Order


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'isbn']
    list_filter = ['title', 'price', 'isbn']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['email', 'status', 'address']
    list_filter = ['email', 'status', 'address']
