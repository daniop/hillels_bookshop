from rest_framework import serializers

from .models import Book, Order


class BookSerializer(serializers.HyperlinkedModelSerializer):

    book_instances = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='book_instance-detail',
        read_only=True
    )

    class Meta:
        model = Book
        fields = ['title', 'isbn', 'price', 'book_instances']


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    order_items = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='order_item-detail',
        read_only=True
    )

    class Meta:
        model = Order
        fields = ['email', 'status', 'address', 'order-items']
