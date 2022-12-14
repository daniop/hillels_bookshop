from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('<int:pk>/comment/', views.book_review, name='book_review'),
    path('genres/<int:pk>/', views.BookListGenreView.as_view(), name='books_by_genre'),
    path('author/<int:pk>/', views.BookListAuthorView.as_view(), name='books_by_author'),
    path('search/', views.book_search, name='book_search'),
    path('contact/', views.contact_form, name='contact'),
    path('login/', views.login_form, name='login'),

]
