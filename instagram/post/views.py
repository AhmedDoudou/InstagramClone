from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url='post:login')
def index(request):
    return render(request, "feed.html")


@login_required(login_url='post:login')
def Profile(request,id):
    user = User.objects.get(id=id)
    users = User.objects.all()
    context = {
        "user":user,
        "users":users
    }
    return render(request,'profile.html', context)

@login_required(login_url='post:login')  
def Chat(request):
    return render(request,"chat.html")
def Register(request):
    if request.user.is_authenticated:
        return redirect('post:home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Account Is Created Successfully')
                return redirect("post:login")
            else :
                messages.error(request,'The Form is Invalid')
        context = {"form":form,}
        return render(request,"register.html",context)
def Trending(request):
    users = User.objects.all()
    context = {
        "users":users
    }
    return render(request,"trending.html",context)
def Login(request):
    if request.user.is_authenticated:
        return redirect('post:home')
    else:
        if request.method == 'POST':
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username= username, password= password)
            if user is not None:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else :
                    return redirect('post:home')
            else:
                messages.error(request, 'Invalid User Name or Password')
        context = {}
        return render(request,"login.html",context)

def Logout(request):
    logout(request)
    return redirect('post:login')