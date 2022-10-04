from django.contrib import admin

from .models import Author, Book, BookInstance, Genre


class GenreInline(admin.TabularInline):
    model = Book.genre.through


class BookInstInline(admin.TabularInline):
    model = BookInstance


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    inlines = [
        GenreInline,
        BookInstInline,
    ]
    exclude = ['genre']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['book_obj', 'status', 'place']
