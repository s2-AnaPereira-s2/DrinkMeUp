from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Representation of the secondary attributes of a User"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    workouts_done = models.IntegerField(default=0)
    latest_post = models.CharField(default="Welcome! Let's drink!", max_length=100)
    spirits = models.CharField(max_length=100, default="Spirits")
    taste = models.CharField(max_length=50, default="Taste")
    boozy = models.CharField(max_length=50, default="Boozy")
    

class Drinks(models.Model):
    cocktail = models.CharField(max_length=50, default="Cocktail")
    spirits = models.CharField(max_length=100, default="Spirit")
    taste = models.CharField(max_length=50, default="Taste")
    boozy = models.CharField(max_length=50, default="Boozy")
    ingredients = models.TextField(default="Ingredients")
    instructions = models.TextField(default="Instructions")
    image = models.ImageField(null=True, blank=True, upload_to="media/cocktails/")
    
class DrinksMade(models.Model):
    user = models.CharField(max_length=50)
    drink = models.ForeignKey(Drinks, on_delete=models.CASCADE, related_name='made_drinks')
    cocktail = models.CharField(max_length=50, null=True)
    rate = models.CharField(max_length=50, blank=True)
    comment = models.TextField(blank=True)
