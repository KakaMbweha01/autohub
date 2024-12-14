from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Car(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    #image_url = models.URLField()
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)
    # define default ordering
    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.name} ({self.brand})"

# model to include a profile picture field
class UserProfile(models.Model):
    PHONE_NUMBER_REGEX = RegexValidator(regex=r'^\+?\d{10,15}$', mesasge="Enter a valid phone number (e.g., +254712345678790).")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[PHONE_NUMBER_REGEX]
    )
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')
    date_of_birth = models.DateField(blank=True, null=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
        ('O', 'Other')
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)