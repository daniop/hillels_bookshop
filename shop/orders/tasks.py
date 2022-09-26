import os

from celery import shared_task

from django.core.mail import send_mail

import requests

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
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(pk=order_id)
    key = os.environ.get('TOKEN_KEY')
    headers = {
        'Authorization': 'Token ' + key,
    }
    url = 'http://stock:8000/orders/'
    params = {
        'email': order.email,
        'address': order.address,
        'order_id_in_shop': order.id,
        'order_items': order.items
    }
    requests.post(url, data=params, headers=headers)
