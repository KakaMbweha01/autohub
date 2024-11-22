from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
    template_name = ['name', 'brand', 'price', 'year', 'description', 'image_url']
