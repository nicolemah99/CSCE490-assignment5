from datetime import date

from django import forms
from django.forms import DateInput, ModelForm, SelectDateWidget
from typing_extensions import Required

from .models import Bid, Comment, Listing


class DateInput(DateInput):
    input_type = 'date'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.setdefault('min', date.today)

class NewListing(ModelForm):

    class Meta:
        model = Listing
        fields = ['name', 'currentBid', 'category', 'description', 'dateBidEnd', 'image']
        widgets = {'dateBidEnd':DateInput(attrs={'type': 'date'}),}

class NewComment(ModelForm):

    class Meta:
        model = Comment
        fields = ['comment']
    
class NewBid(ModelForm):

    class Meta:
        model = Bid
        fields = ['bidPrice']

