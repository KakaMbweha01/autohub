from django import forms
from .models import Car
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'brand', 'year', 'price', 'description', 'image']

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
