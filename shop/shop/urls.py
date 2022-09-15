from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
]
