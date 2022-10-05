from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import ClientChangeForm, ClientCreationForm
from .models import Author, Book, Client, Genre, Review


@admin.action(description='Одобрить отзыв')
def make_active(modeladmin, request, queryset):
    queryset.update(active=True)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'book', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
    actions = [make_active]


@admin.register(Client)
class ClientAdmin(UserAdmin):
    model = Client
    add_form = ClientCreationForm
    form = ClientChangeForm
    list_display = ('email', 'username', 'is_staff', 'is_active', 'last_name')
    list_filter = ('email', 'username', 'is_staff', 'is_active',)
    search_fields = ['username', 'email','last_name']
    
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal Information', {'fields': ('first_name', 'last_name')}),
        ('Address Information', {'fields': ('city', 'postal_code', 'address')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Groups', {'fields': ('groups',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email',),
        }),
    )

