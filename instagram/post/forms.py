from django.contrib.auth.forms import UserCreationForm 
from django import forms
from django.contrib.auth.models import User
from .models import *



class CreateUserForm(UserCreationForm):
    class Meta :
        model = User
        fields = ["username","email","password1","password2"]


# class PostForm(forms.Form):
#     class Meta :
#         model = Post
#         fields = "__all__"

class PostForm(forms.ModelForm):
    picture = forms.ImageField(required=True)
    caption = forms.CharField(required=True, max_length=100,widget=forms.TextInput(attrs={'class': 'shadow-none bg-gray-100','placeholder': 'Your Caption ...'}))
    tag = forms.CharField(required=True, max_length=100,widget=forms.TextInput(attrs={'class': 'shadow-none bg-gray-100','placeholder': 'Your Tags separed by camma ...'}))

    class Meta:
        model = Post
        fields = ['picture', 'caption', 'tag']

