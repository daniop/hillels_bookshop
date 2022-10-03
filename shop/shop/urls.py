from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('genres/<int:pk>/', views.books_by_genre, name='books_by_genre'),
    path('search/', views.book_search, name='book_search')
]
