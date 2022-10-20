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
from datetime import date

class Category(models.Model):
    name = models.CharField(max_length = 64)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"

class User(AbstractUser):
    pass


class Listing(models.Model):
    name = models.CharField(max_length= 64)
    currentBid = models.DecimalField(max_digits=19, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default= 1, on_delete=models.SET_DEFAULT)
    category = models.ForeignKey(Category, default = "", on_delete = models.SET_DEFAULT)
    description = models.TextField(max_length= 200,default = "")
    datePosted = models.DateField(default=date.today)
    dateBidEnd = models.DateField(default=date.today)
    image = models.ImageField(upload_to= 'images', default='images')

    def __str__(self):
        return f"{self.name}"

class Comment(models.Model):
    comment = models.TextField(max_length = 200)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, default = "", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} commented on {self.listing}'

class Bid(models.Model):
    bidPrice = models.DecimalField(max_digits=19, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default= 1, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, default = "", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now= True)

    def __str__(self):
        return f'Bid on {self.listing} for {self.bidPrice}'

#Need models for:
#Categories
#Watchlist
#Bid
#Comments