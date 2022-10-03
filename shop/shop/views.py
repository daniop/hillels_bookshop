from cart.forms import CartAddProductForm

from django.contrib.postgres.search import TrigramSimilarity, SearchVector
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .filters import BookFilter
from .forms import SearchForm
from .models import Book, Genre


class BookListView(generic.ListView):
    template_name = 'shop/book/list.html'
    context_object_name = 'books'
    queryset = Book.objects.filter(available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['filter'] = BookFilter(self.request.GET, queryset=self.queryset)
        context['search_form'] = SearchForm()
        return context


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'shop/book/detail.html'

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        context['search_form'] = SearchForm()
        return context


def books_by_genre(request, pk):
    genre = get_object_or_404(Genre, id=pk)
    qs = Book.objects.filter(genre=genre)
    genres = Genre.objects.all()
    f = BookFilter(request.GET, queryset=qs)
    search_form = SearchForm()
    return render(request, 'shop/book/books_by_genre.html', {
        'books': qs, 'genre': genre, 'genres': genres, 'filter': f, 'search_form': search_form
    })


def book_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Book.objects.annotate(
                search = SearchVector('title'),).filter(search=query)

    return render(request,
                  'shop/book/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})
