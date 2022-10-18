from datetime import datetime
from email.policy import default
from pyexpat import model
from unicodedata import category
from unittest.util import _MAX_LENGTH
from xmlrpc.client import DateTime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.forms import ModelForm, SelectDateWidget, TextInput
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length = 64)

    def __str__(self):
        return f"{self.name}"

class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(max_length= 64)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default= 1, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, default = "", on_delete = models.CASCADE)
    description = models.TextField(max_length= 200,default = "")

    def __str__(self):
        return f"{self.name} posted for {self.price}"


#Need models for:
#Listings
#Categories
#Watchlist
#Bid