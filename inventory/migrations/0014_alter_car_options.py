# Generated by Django 5.1.3 on 2025-01-02 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_alter_userprofile_favorite_cars_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='car',
            options={'ordering': ['name']},
        ),
    ]
