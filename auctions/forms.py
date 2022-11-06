from typing_extensions import Required
from django import forms
from django.forms import ModelForm, SelectDateWidget
from .models import Listing, Comment, Bid, DateInput, date


class DateInput(DateInput):
    input_type = 'date'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.setdefault('min', date.today)


class NewListing(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['name', 'currentBid', 'category',
                  'description', 'dateBidEnd', 'image']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Name'}),
                   'currentBid': forms.NumberInput(attrs={'class': 'form-control form-control'}),
                   'category': forms.Select(attrs={'class': 'form-control'}),
                   'description': forms.Textarea(attrs={'class': 'form-control'}),
                   'dateBidEnd': DateInput(attrs={'type': 'date'}),
                   'image': forms.FileInput(attrs={'class': 'form-control-file'})}


class NewComment(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class NewBid(ModelForm):
    class Meta:
        model = Bid
        fields = ['bidPrice']
