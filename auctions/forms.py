from typing_extensions import Required
from django import forms
from django.forms import ModelForm, SelectDateWidget
from django import forms
from .models import Listing

class NewListing(ModelForm):
    name = forms.TextInput()
    description = forms.TextInput()
    price = forms.TextInput()
    category = forms.TextInput()
    user = forms.TextInput()
    dateBidEnd = forms.DateField(widget=forms.SelectDateWidget())


    class Meta:
        model = Listing
        fields = ['name', 'price', 'category', 'description', 'dateBidEnd']
