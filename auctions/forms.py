from typing_extensions import Required
from django import forms
from django.forms import ModelForm
from django import forms
from .models import Listing

class NewListing(ModelForm):
    name = forms.TextInput()
    price = forms.TextInput()
    user = forms.TextInput()
    category = forms.TextInput()

    class Meta:
        model = Listing
        fields = ['name', 'price', 'user', 'category']