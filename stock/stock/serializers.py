from book.models import Author, Book, BookInstance, Genre

from rest_framework import serializers

from .models import Order, OrderItem


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name']


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


class BookSerializer(serializers.HyperlinkedModelSerializer):
    bookinstances = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='bookinstance-detail',
        read_only=True,
    )
    author = serializers.CharField(read_only=True)
    genre = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'price', 'genre', 'summary', 'author', 'bookinstances']


class BookInstSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = BookInstance
        fields = ['status', 'place', 'book_obj']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['quantity', 'book_obj', 'price']


class OrderSerializer(serializers.ModelSerializer):
    orderitems = OrderItemSerializer(many=True)

    def create(self, validated_data):
        items_data = validated_data.pop('orderitems')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            book_obj = item_data['book_obj']
            OrderItem.objects.create(
                order=order, book_obj=book_obj, quantity=item_data['quantity'], price=item_data['price']
            )
        return order

    class Meta:
        model = Order
        fields = [
            'email',
            'status',
            'address',
            'order_id_in_shop',
            'first_name',
            'last_name',
            'city',
            'postal_code',
            'orderitems']
