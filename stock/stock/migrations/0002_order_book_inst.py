# Generated by Django 4.1.1 on 2022-09-28 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='book_inst',
            field=models.ManyToManyField(blank=True, to='book.bookinstance'),
        ),
    ]