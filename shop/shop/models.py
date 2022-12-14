from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from .tasks import review_active


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.last_name}, {self.first_name}"

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])


class Genre(models.Model):
    """Model representing a book genre (e.g. Science Fiction, Non Fiction)."""
    name = models.CharField(max_length=200)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000)
    genre = models.ManyToManyField(Genre, blank=True)
    isbn = models.CharField(max_length=13)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    book_id_in_stock = models.IntegerField(verbose_name='Номер книги на складе', null=True)
    quantity_in_stock = models.IntegerField(verbose_name='Количество книг на складе', null=True)

    class Meta:
        ordering = ['title', 'author']

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('shop:book_detail', args=[str(self.id)])


class Review(models.Model):
    book = models.ForeignKey(Book,
                             on_delete=models.CASCADE,
                             related_name='reviews')
    name = models.CharField(max_length=80, verbose_name='Ваше имя')
    email = models.EmailField(max_length=250, verbose_name='E-mail')
    body = models.TextField(verbose_name='Сообщение')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Review by {self.name} on {self.book}'

    def save(self, *args, **kwargs):
        super(Review, self).save(*args, **kwargs)
        link = self.book.get_absolute_url()
        if self.active:
            message = f'Новый отзыв к книге {self.book.title} от {self.name}. {link}'
            review_active.delay("New review", self.email, message)


class Client(AbstractUser):
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=80, verbose_name='Ваш адрес.')
    first_name = models.CharField(max_length=80, verbose_name='Ваше имя')
    last_name = models.CharField(max_length=80, verbose_name='Ваша фамилия')
    city = models.CharField(max_length=80, verbose_name='Ваш город')
    postal_code = models.IntegerField(verbose_name='Индекс', null=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.username
