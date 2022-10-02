from django import forms
from django.contrib.auth.models import User
from .models import *
from user_profile.models import *


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']



#   profile_pic = forms.ImageField(required=True)
#     first_name  = forms.CharField( max_length=100,widget=forms.TextInput(attrs={'class': 'shadow-none bg-gray-100','placeholder': 'Your First Name ...'}))
#     last_name   = forms.CharField( max_length=100,widget=forms.TextInput(attrs={'class': 'shadow-none bg-gray-100','placeholder': 'Your Last Name  ...'}))
#     location    = forms.CharField( max_length=100,widget=forms.TextInput(attrs={'class': 'shadow-none bg-gray-100','placeholder': 'Location ...'}))
#     url         = forms.CharField( max_length=100,widget=forms.TextInput(attrs={'class': 'shadow-none bg-gray-100','placeholder': 'URL ...'}))
#     bio         = forms.CharField( max_length=100,widget=forms.Textarea(attrs={'class': 'bg-gray-100 shadow-none border mt-2 w-full px-3 py-2 rounded-md focus:border-blue-600 ','placeholder': 'Bio ...'}))











