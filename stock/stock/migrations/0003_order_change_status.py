# Generated by Django 4.1.1 on 2022-09-28 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_order_book_inst'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='change_status',
            field=models.BooleanField(default=False),
        ),
    ]
