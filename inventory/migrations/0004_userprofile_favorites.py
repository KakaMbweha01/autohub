# Generated by Django 5.1.3 on 2024-12-17 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_alter_car_options_review_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorited_by', to='inventory.car'),
        ),
    ]