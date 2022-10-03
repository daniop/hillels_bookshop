import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt', label='Цена выше')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt', label='Цена ниже')

    class Meta:
        model = Book
        fields = ['author', 'price__gt', 'price__lt']

    def __init__(self, *args, **kwargs):
        super(BookFilter, self).__init__(*args, **kwargs)
        self.filters['author'].label = "Автор"
