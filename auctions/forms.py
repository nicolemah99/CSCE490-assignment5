from typing_extensions import Required
from django import forms
from django.forms import ModelForm, SelectDateWidget
from .models import *

class NewListing(ModelForm):

    class Meta:
        model = Listing
        fields = ['name', 'currentBid', 'category', 'description', 'dateBidEnd', 'image']

class NewComment(ModelForm):

    class Meta:
        model = Comment
        fields = ['comment']
    
class NewBid(ModelForm):

    class Meta:
        model = Bid
        fields = ['bidPrice']

