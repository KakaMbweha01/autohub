from rest_framework import serializers
from .models import Car, UserProfile, Review, Notification

# car serializer
class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'name', 'brand', 'price', 'year', 'description', 'image']

# user profile serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'favorite_cars', 'profile_picture']

# review serializer
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

# favorites serializer
class FavoriteSerializer(serializers.ModelSerializer):
    car = serializers.StringRelatedField()

    class Meta:
        #model = Favorite # I have to make a favorite model
        fields = ['id', 'user', 'car', 'added_date']

# notification serializer
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'is_read', 'created_at']