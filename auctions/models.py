from pyexpat import model
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(max_length= 64)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    #datePosted = models.DateTimeField(auto_now_add=True)
    #bidClosed = models.DateTimeField()
    #owner = models.ForeignKey(User(),on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} posted for {self.price}"

#Need models for:
#Listings
#Categories
#Watchlist
#Bid