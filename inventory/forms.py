from django import forms
from .models import Car, UserProfile, Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from datetime import date

# modelform for adding cars
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'brand', 'year', 'price', 'description', 'image']

# modelform for user registration
class UserRegistrationForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

# modelForm for creating a userprofile
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'profile_picture', 'date_of_birth', 'gender']

        def clean_phone_number(self):
            phone_number = self.cleaned_data.get('phone_number')
            if phone_number and UserProfile.objects.filter(phone_number=phone_number).exclude(user=self.instance.user).exists():
                raise forms.ValidationError("This phone number is already in use.")
            return phone_number

        def clean_date_of_birth(self):
            dob = self.cleaned_data.get('date_of_birth')
            if dob and dob >= date.today():
                raise forms.ValidationError("The date of birth cannot be in the future.")
            return dob

        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }

# modelForm to create a way to contact the user
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

# modelForm to make a review
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']