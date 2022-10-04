from cart.forms import CartAddProductForm

from django.contrib.postgres.search import SearchVector
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views import generic
from django.views.decorators.http import require_POST

from .filters import BookFilter
from .forms import ContactForm, ReviewForm, SearchForm
from .models import Book, Genre
from .tasks import send_contact, new_review


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
        objects_list = self.object.reviews.filter(active=True)
        page_num = self.request.GET.get('page', 1)
        paginator = Paginator(objects_list, 3)
        total_comments = objects_list.count()
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context['page_obj'] = page_obj
        if self.request.user.is_authenticated:
            context['form'] = ReviewForm(
                initial={'email': self.request.user.email, 'name': self.request.user.username}
            )
        else:
            context['form'] = ReviewForm()
        context['total_comments'] = total_comments
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
            results = Book.objects.annotate(search=SearchVector('title'), ).filter(search=query)

    return render(request,
                  'shop/book/search.html',
                  {'search_form': form,
                   'query': query,
                   'results': results,
                   'cart_product_form': cart_product_form,
                   })


def contact(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_contact.delay(name, email, message)
            data['form_is_valid'] = True
            msg = [f"Сообщение от {name} отправлено"]
            data['msg_list'] = render_to_string('shop/message.html', {
                'messages': msg
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
    else:
        form = ContactForm()
    return contact(request, form, 'shop/book/contact.html')


@require_POST
def book_review(request, pk):
    book = get_object_or_404(Book, id=pk)
    review = None
    form = ReviewForm(data=request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.book = book
        review.save()
        message = f'Новый отзыв к книге: {book.title} от {review.name}- {review.body}'
        new_review.delay("New comment", message)

    return render(request, 'shop/book/review.html',
                  {'book': book,
                   'form': form,
                   'review': review})
