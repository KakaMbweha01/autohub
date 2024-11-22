class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'year') # Display columns
    search_fields = ('name', 'brand') # Searchable fields

admin.site.register(Car, CarAdmin)