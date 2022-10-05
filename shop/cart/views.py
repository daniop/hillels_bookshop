from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from shop.forms import SearchForm
from shop.models import Book, Genre

from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, pk):
    cart = Cart(request)
    book = get_object_or_404(Book, id=pk)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        if cd['quantity'] > book.quantity_in_stock:
            messages.warning(request, f'Книга {book.title} доступна в {book.quantity_in_stock} экземплярах')
            return redirect('shop:book_detail', book.id)
        cart.add(book=book,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, pk):
    cart = Cart(request)
    book = get_object_or_404(Book, id=pk)
    cart.remove(book)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    search_form = SearchForm()
    genres = Genre.objects.all()
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})

    return render(request,
                  'cart/detail.html',
                  {'cart': cart,
                   'search_form': search_form,
                   'genres': genres})
