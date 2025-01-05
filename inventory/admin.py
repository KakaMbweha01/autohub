from django.contrib import admin
from .models import Car, Notification, Favorite

# Register your models here.

class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'year', 'price') # fields to display in the listvew
    search_fields = ('name', 'brand') # add a search bar for specific fields
    list_filter = ('brand', 'year') # Add filters for specific fields

admin.site.register(Car)

#@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('message', 'user__username')

admin.site.register(Notification)

#@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'added_date')
    list_filter = ('added_date')
    search_fields = ('user__username', 'car__name')

admin.site.register(Favorite)