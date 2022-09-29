from book.models import Book, BookInstance

from django.db import models


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
    book_inst = models.ManyToManyField(BookInstance, blank=True)
    change_status = models.BooleanField(default=False, verbose_name='Обновить книги')

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

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        if self.change_status:
            for book in self.book_inst.all():
                book.update_status()
        self.change_status = False


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='orderitems', on_delete=models.CASCADE)
    book_obj = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.book_obj.title)

    def get_cost(self):
        return self.price * self.quantity
