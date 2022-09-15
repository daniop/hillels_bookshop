from cart.forms import CartAddProductForm

from django.shortcuts import render
from django.views import generic

from .models import Book


def book_list(request):
    books = Book.objects.filter(available=True)
    return render(request,
                  'shop/book/list.html',
                  {'books': books})


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'shop/book/detail.html'

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        return context
