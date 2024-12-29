from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
# car model
class Car(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    #image_url = models.URLField()
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)
    #favorite_cars = models.ManyToManyField(User, blank=True, related_name='favorited_by')
    #favorited_by = models.ManyToManyField(User, related_name='wishlist', blank=True)
    # define default ordering
    class Meta:
        ordering = ['id']

    def average_rating(self):
        reviews = self.reviews.all() # Related reviews using the 'related_name'
        if reviews.exists():
            return round(sum(review.rating for review in reviews) / reviews.count(), 1)
        return 0 # No reviews yet

    def __str__(self):
        return f"{self.name} ({self.brand})"

# user profile model, has a profile picture field
class UserProfile(models.Model):
    PHONE_NUMBER_REGEX = RegexValidator(regex=r'^\+?\d{10,15}$', message="Enter a valid phone number (e.g., +254712345678790).")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[PHONE_NUMBER_REGEX]
    )
    address = models.TextField(blank=True, null=True)
    favorite_cars = models.ManyToManyField(Car, related_name='favorited_by') # new favorites field
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')
    date_of_birth = models.DateField(blank=True, null=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.user.username # Access the username of the associated user

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

# Review model
class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)]) # ratings between 1 and 5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}- {self.rating}"

# notification model for user notifications
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False) # has the user read the notifications
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"