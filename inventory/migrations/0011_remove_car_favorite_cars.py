# Generated by Django 5.1.3 on 2024-12-25 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_remove_car_favorited_by_remove_car_favorites_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='favorite_cars',
        ),
    ]