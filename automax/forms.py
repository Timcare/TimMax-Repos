from django import forms
from dataclasses import field
from .models import Listing
from users.models import Location
from django.contrib.auth.models import User
from users.models import Profile
from .widgets import CustomPictureImageFieldWidget
class UserForm(forms.ModelForm):
    username=forms.CharField(disabled=True)
    email=forms.CharField(required=True)
    first_name=forms.CharField(required=True)
    class Meta:
        model=User
        fields=("username","email", "first_name","last_name")

class ProfileForm(forms.ModelForm):
    photo = forms.ImageField()
    bio=forms.CharField(widget=forms.Textarea)

    class Meta:
        model=Profile
        fields=("photo","bio","phone_number")

class ListingForm(forms.ModelForm):

    class Meta:
        model=Listing
        fields=('brand','model','vin','mileage','color','description','engine','transmission','image')

class LocationForm(forms.ModelForm):
    address_1=forms.CharField(required=True)
    class Meta:
        model=Location
        fields=('address_1','address_2','city','state','zip_code')