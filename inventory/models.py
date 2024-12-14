from django.db import models

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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')
