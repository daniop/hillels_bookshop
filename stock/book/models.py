from django.db import models


class AvailableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='available')


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.last_name}, {self.first_name}"


class Genre(models.Model):
    """Model representing a book genre (e.g. Science Fiction, Non Fiction)."""
    name = models.CharField(max_length=200)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000)
    genre = models.ManyToManyField(Genre, blank=True)
    isbn = models.CharField(max_length=13)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


class BookInstance(models.Model):
    place_choices = (
        ('top_cab', 'Верхний шкаф'),
        ('bottom_cab', 'Нижний шкаф'),
    )

    status_choies = (
        ('available', 'Доступно'),
        ('sold', 'Продано')
    )

    book_obj = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, related_name='bookinstances')
    place = models.CharField(max_length=15,
                             choices=place_choices,
                             default='top_cab',
                             verbose_name='Место хранения')
    status = models.CharField(max_length=15,
                              choices=status_choies,
                              default='available',
                              verbose_name='Статус')

    objects = models.Manager()
    available = AvailableManager()

    def update_status(self):
        if self.status == 'available':
            self.status = 'sold'
        elif self.status == 'sold':
            self.status = 'available'
        self.save()

    def __str__(self):
        return f'{str(self.book_obj)}({self.id}): {self.status}'
