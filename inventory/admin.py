from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Car

class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'year', 'price') # fields to display in the listvew
    search_fields = ('name', 'brand') # add a search bar for specific fields
    list_filter = ('brand', 'year') # Add filters for specific fields

admin.site.register(Car)