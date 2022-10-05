import os

from celery import shared_task

from django.core.mail import send_mail

import requests

from shop.models import Author, Book, Genre

from .models import Order


@shared_task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(pk=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject,
                          message,
                          'admin@myshop.com',
                          [order.email])
    return mail_sent


@shared_task
def order_to_stock(order_id):
    order = Order.objects.get(pk=order_id)
    key = os.environ.get('TOKEN_KEY')
    headers = {
        'Authorization': 'Token ' + key,
    }
    url = 'http://stock:8000/api/orders/'
    order_items_list = []
    for item in order.items.all():
        temp_dict = dict()
        temp_dict['price'] = str(item.price)
        temp_dict['quantity'] = item.quantity
        temp_dict['book_obj'] = item.books.book_id_in_stock
        order_items_list.append(temp_dict)
    params = {
        'email': order.email,
        'address': order.address,
        'order_id_in_shop': order.id,
        'first_name': order.first_name,
        'last_name': order.last_name,
        'city': order.city,
        'postal_code': order.postal_code,
        'orderitems': order_items_list,
    }
    requests.post(url, json=params, headers=headers)


@shared_task
def update_genre():
    url = 'http://stock:8000/api/genres/'
    r = requests.get(url).json()
    create_list = []
    for genre in r['results']:
        if not Genre.objects.filter(name=genre['name']).exists():
            create_list.append(Genre(name=genre['name']))
    Genre.objects.bulk_create(create_list)


@shared_task
def update_author():
    url = 'http://stock:8000/api/authors/'
    r = requests.get(url).json()
    create_list = []
    for author in r['results']:
        if not Author.objects.filter(first_name=author['first_name'], last_name=author['last_name']).exists():
            create_list.append(Author(first_name=author['first_name'], last_name=author['last_name']))
    Author.objects.bulk_create(create_list)


@shared_task
def create_books():
    url = 'http://stock:8000/api/books/'
    r = requests.get(url).json()
    for book in r['results']:
        if not Book.objects.filter(isbn=book['isbn']).exists():
            author = book['author'].split(', ')
            new_book = Book.objects.create(
                title=book['title'],
                author=Author.objects.get(first_name=author[1], last_name=author[0]),
                summary=book['summary'],
                isbn=book['isbn'],
                price=book['price'],
                book_id_in_stock=book['id'],
                quantity_in_stock=len(book['bookinstances']),
                available=True if len(book['bookinstances']) else False
            )
            for genre in book['genre']:
                genre = Genre.objects.get(name=genre)
                new_book.genre.add(genre)


@shared_task
def update_books():
    url = 'http://stock:8000/api/books/'
    r = requests.get(url).json()
    for book in r['results']:
        if Book.objects.filter(isbn=book['isbn']).exists():
            Book.objects.filter(isbn=book['isbn']).update(
                title=book['title'],
                summary=book['summary'],
                price=book['price'],
                book_id_in_stock=book['id'],
                quantity_in_stock=len(book['bookinstances']),
                available=True if len(book['bookinstances']) else False)


@shared_task
def update_orders():
    url = 'http://stock:8000/api/orders/'
    r = requests.get(url).json()
    update_list = []
    for obj in r['results']:
        order = Order.objects.get(pk=obj['order_id_in_shop'])
        order.status = obj['status']
        update_list.append(order)
    Order.objects.bulk_update(update_list, ['status'])
