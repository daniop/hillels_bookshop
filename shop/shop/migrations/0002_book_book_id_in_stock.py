# Generated by Django 4.1.1 on 2022-09-19 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_id_in_stock',
            field=models.IntegerField(null=True, verbose_name='Номер книги на складе'),
        ),
    ]