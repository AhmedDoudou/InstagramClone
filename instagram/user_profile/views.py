from .models import Profile
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.urls import resolve
from post.models import Post


def UserProfile(request,username):
    user        = get_object_or_404(User,username=username) # get user 
    profile     = Profile.objects.get(user=user)    # get user profile
    url_name    = resolve(request.path).url_name   # get the path 
    if url_name == 'profile':
        posts   = Post.objects.filter(user=user).order_by('-posted')
    else:
        return redirect("post:home")
    #pagination
    paginator = Paginator(posts,3)
    page_number =request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)
    context = {
        'posts_paginator':posts_paginator,
        'posts':posts,
        'user':user,
        
    }
    return render(request,"user/profile.html",context)







# Create your views here.
