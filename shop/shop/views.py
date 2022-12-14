from cart.forms import CartAddProductForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, views
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.postgres.search import SearchVector
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST


from .filters import BookFilter
from .forms import ClientCreationForm, ContactForm, LoginForm, ReviewForm, SearchForm
from .models import Author, Book, Client, Genre
from .tasks import new_review, send_contact


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
        sort_by = self.request.GET.get('sort')
        sort = 'created'
        if sort_by == 'priceup':
            sort = 'price'
        elif sort_by == 'pricedown':
            sort = '-price'
        elif sort_by == 'nameup':
            sort = 'title'
        elif sort_by == 'namedown':
            sort = '-title'
        elif sort_by == 'dateup':
            sort = 'created'
        elif sort_by == 'datedown':
            sort = '-created'
        return BookFilter(self.request.GET, queryset=queryset).qs.order_by(sort).select_related('author')


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
        sort_by = self.request.GET.get('sort')
        sort = 'created'
        if sort_by == 'priceup':
            sort = 'price'
        elif sort_by == 'pricedown':
            sort = '-price'
        elif sort_by == 'nameup':
            sort = 'title'
        elif sort_by == 'namedown':
            sort = '-title'
        elif sort_by == 'dateup':
            sort = 'created'
        elif sort_by == 'datedown':
            sort = '-created'
        return BookFilter(self.request.GET, queryset=queryset).qs.order_by(sort).select_related('author')


class BookListAuthorView(generic.ListView):
    model = Book
    template_name = 'shop/book/books_by_author.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['cart_product_form'] = CartAddProductForm()
        context['filter'] = BookFilter(self.request.GET, queryset=self.get_queryset())
        context['search_form'] = SearchForm()
        context['author'] = Author.objects.get(pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(author__id=self.kwargs['pk'])
        sort_by = self.request.GET.get('sort')
        if sort_by == 'priceup':
            queryset = queryset.order_by('price')
        elif sort_by == 'pricedown':
            queryset = queryset.order_by('-price')
        elif sort_by == 'nameup':
            queryset = queryset.order_by('title')
        elif sort_by == 'namedown':
            queryset = queryset.order_by('-title')
        elif sort_by == 'dateup':
            queryset = queryset.order_by('created')
        elif sort_by == 'datedown':
            queryset = queryset.order_by('-created')
        return BookFilter(self.request.GET, queryset=queryset).qs.select_related('author')


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
            results = Book.objects.annotate(
                search=SearchVector('title', 'author__last_name', 'author__first_name'),
            ).filter(search=query)

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
            msg = [f"?????????????????? ???? {name} ????????????????????"]
            data['msg_list'] = render_to_string('shop/message_contact.html', {
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
        message = f'?????????? ?????????? ?? ??????????: {book.title} ???? {review.name}- {review.body}'
        new_review.delay("New comment", message)

    return render(request, 'shop/book/review.html',
                  {'book': book,
                   'form': form,
                   'review': review})


class UserProfile(LoginRequiredMixin, generic.DetailView):
    model = Client
    template_name = "registration/profile.html"

    def get_context_data(self, **kwargs):
        genres = Genre.objects.all()
        context = super(UserProfile, self).get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        context['search_form'] = SearchForm()
        context['genres'] = genres
        context['orders'] = self.object.orders.all()
        return context

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class SignUpView(generic.CreateView):
    form_class = ClientCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("shop:book_list")

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)  # TODO: fix
        return super(SignUpView, self).form_valid(form)


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Client
    fields = ["first_name", "last_name", "email", "username", "city", "address", "postal_code"]
    template_name = "registration/update_profile.html"
    success_url = reverse_lazy("profile")
    success_message = "?????????????? ????????????????"

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class PasswordsChangeViewCustom(views.PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')
    template_name = 'registration/change-password_custom.html'


def password_success(request):
    return render(request, 'registration/change_pass_done.html')


def custom_login_page(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'?????????? ???????????????????? {user.username}'
                data['form_is_valid'] = True
                messages.success(request, message)
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def login_form(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
    else:
        form = LoginForm()
    return custom_login_page(request, form, 'registration/custom_login.html')
