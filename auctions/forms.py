from typing_extensions import Required
from django import forms
from django.forms import ModelForm, SelectDateWidget
from django import forms
from .models import *

class NewListing(ModelForm):
    name = forms.TextInput()
    description = forms.TextInput()
    startingBid = forms.DecimalField()
    category = forms.TextInput()
    dateBidEnd = forms.DateField(widget=forms.SelectDateWidget())
    image = forms.ImageField()


    class Meta:
        model = Listing
        fields = ['name', 'startingBid', 'category', 'description', 'dateBidEnd', 'image', 'user']

class NewComment(ModelForm):
    comment = forms.TextInput()

    class Meta:
        model = Comment
        fields = ['comment', 'listing', 'user']
    
class NewBid(ModelForm):
    bidPrice = forms.DecimalField()

    class Meta:
        model = Bid
        fields = ['bidPrice', 'user', 'listing']

