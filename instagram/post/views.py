from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def index(request):
    return render(request, "trending.html")

def Register(request):
    form = UserCreationForm()
    context = {"form":form}
    return render(request,"form-register.html",context)

def Login(request):
    context = {}
    return render(request,"form-login.html",context)