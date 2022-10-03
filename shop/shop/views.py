from cart.forms import CartAddProductForm

from django.contrib.postgres.search import SearchVector
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from django.views import generic


from .filters import BookFilter
from .forms import SearchForm
from .models import Book, Genre


class BookListView(generic.ListView):
    model = Book
    template_name = 'shop/book/list.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['cart_product_form'] = CartAddProductForm()
        context['filter'] = BookFilter(self.request.GET, queryset=self.get_queryset())
        context['search_form'] = SearchForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return BookFilter(self.request.GET, queryset=queryset).qs


class BookListGenreView(generic.ListView):
    model = Book
    template_name = 'shop/book/books_by_genre.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['cart_product_form'] = CartAddProductForm()
        context['filter'] = BookFilter(self.request.GET, queryset=self.get_queryset())
        context['search_form'] = SearchForm()
        context['genre'] = Genre.objects.get(pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(genre__id=self.kwargs['pk'])
        return BookFilter(self.request.GET, queryset=queryset).qs


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'shop/book/detail.html'

    def get_context_data(self, **kwargs):
        genres = Genre.objects.all()
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        context['search_form'] = SearchForm()
        context['genres'] = genres
        return context


def book_search(request):
    form = SearchForm()
    query = None
    results = []
    cart_product_form = CartAddProductForm()

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Book.objects.annotate(search=SearchVector('title'),).filter(search=query)

    return render(request,
                  'shop/book/search.html',
                  {'search_form': form,
                   'query': query,
                   'results': results,
                   'cart_product_form': cart_product_form,
                   })
