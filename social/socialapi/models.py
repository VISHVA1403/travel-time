from django.db import models
from django.contrib.auth.models import User


class Destination(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.name + " - " + self.country
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True,default='E:\Django\social\media\profile_pictures\defaultuser.png')
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)
    bio = models.TextField(blank=True,default='bio')
    favorite_destinations = models.ManyToManyField(Destination, blank=True)
    travel_style = models.CharField(max_length=100, blank=True)
    wishlist = models.ManyToManyField(Destination, related_name='wishlisted_by', blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.user.username




