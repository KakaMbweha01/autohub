# Generated by Django 5.1.3 on 2024-12-22 08:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_car_favorited_by_alter_car_favorites_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorite_cars', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorite_cars', to='inventory.car'),
        ),
    ]
