from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


class BookInstance(models.Model):
    place_choices = (
        ('top_cab', 'Верхний шкаф'),
        ('bottom_cab', 'Нижний шкаф'),
    )

    book_obj = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    place = models.CharField(max_length=15,
                             choices=place_choices,
                             default='top_cab',
                             verbose_name='Место хранения')

    def __str__(self):
        return str(self.id)


class Order(models.Model):
    status_choices = (
        ('in_work', 'В работе'),
        ('success', 'Успешно отправлен'),
        ('fail', 'Не отправлен'),
    )

    order_id_in_shop = models.IntegerField(verbose_name='Номер заказа в магазине')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15,
                              choices=status_choices,
                              default='in_work',
                              verbose_name='Статус заказа')

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book_obj = models.ForeignKey(Book, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    book_inst = models.ManyToManyField(BookInstance)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
