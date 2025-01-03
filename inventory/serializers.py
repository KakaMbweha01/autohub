#from rest_framework import serializers
from .models import Car, UserProfile

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'name', 'brand', 'price', 'year', 'description', 'image']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'favorite_cars']