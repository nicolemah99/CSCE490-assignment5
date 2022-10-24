from email.policy import default
from pyexpat import model
from tabnanny import verbose
from tkinter import Widget
from unicodedata import category
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from datetime import date
from django import forms
from pkg_resources import require

class User(AbstractUser):
    pass

class Category(models.Model):
    image = models.ImageField(upload_to= 'auctions/images', default='auctions/images/noimage.jpeg',blank = True, verbose_name = "Images")
    name = models.CharField(max_length = 64)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"



class Listing(models.Model):
    name = models.CharField(max_length= 64)
    currentBid = models.DecimalField(max_digits=19, decimal_places=2, verbose_name = "Starting Bid")
    finalBid = models.DecimalField(max_digits=19, decimal_places=2, null = True, blank = True,verbose_name = "Sold for")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1 , on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null= True, on_delete = models.CASCADE)
    description = models.TextField(max_length= 200,null= True)
    datePosted = models.DateField(default=date.today, verbose_name = "Date Posted")
    dateBidEnd = models.DateField(default=date.today, verbose_name = "End Date")
    image = models.ImageField(upload_to= 'auctions/images', default='auctions/images/noimage.jpeg',blank = True, verbose_name = "Images")
    active = models.BooleanField(default=1)
    winner = models.ForeignKey(User, null=True , on_delete=models.CASCADE, related_name = "winner", blank = True, verbose_name = "Sold to")
    
    def __str__(self):
        return f"{self.name}"


class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, default = "", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} added {self.listing} to watchlist.'

class Comment(models.Model):
    comment = models.TextField(max_length = 200)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, default = "", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} commented on {self.listing}'

class Bid(models.Model):
    bidPrice = models.DecimalField(max_digits=19, decimal_places=2, verbose_name = "Bid Amount")
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