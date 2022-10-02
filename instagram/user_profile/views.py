from django.http import HttpResponseRedirect
from django.db import transaction
from .models import Profile
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.urls import resolve, reverse
from post.models import Post,Stream, Follow
from .forms import *


def UserProfile(request,username):
    user        = get_object_or_404(User,username=username) # get user 
    profile     = Profile.objects.get(user=user)    # get user profile
    url_name    = resolve(request.path).url_name   # get the path 
    if url_name == 'profile':
        posts   = Post.objects.filter(user=user).order_by('-posted')
    else:
        return redirect("post:home")
    # Status
    following   = Follow.objects.all().filter(follower=user)
    follower    = Follow.objects.all().filter(following=user)
    follow_status      = Follow.objects.filter(following=user, follower=request.user).exists()
    #pagination
    paginator = Paginator(posts,3)
    page_number =request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)
    context = {
        'posts_paginator':posts_paginator,
        'posts':posts,
        'profile':profile,
        'user':user,
        'following':following,
        'follower':follower,
        'follow_status':follow_status,

    }
    return render(request,"user/profile.html",context)


def EditProfile(request,username):
    user    = request.user
    profile = Profile.objects.get(user=user)
    form    = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "The Profile is Edited Successfully!")
            return redirect("user:profile", user.username)
    else:
        form = ProfileForm(instance=profile)
        messages.error(request, "form is invalid !!!!!  ")

    context = {
        'form':form,
        'profile':profile
    }
    return render(request,"user/edit.html" ,context)


def FollowAction(request,username,option):
    user = request.user
    following = get_object_or_404(User,username=username) 
    try:
        f,created = Follow.objects.get_or_create(follower=user,following=following)
        if int(option) == 0:
            f.delete()
            Stream.objects.filter(user=user,following=following).all().delete()
        else:
            posts = Post.objects.filter(user=following)[:5]
            with transaction.atomic():
                for post in posts:
                    stream = Stream(following=following,user=user,post=post,date=post.posted)
                    stream.save()
        return HttpResponseRedirect(reverse("user:profile", args=[username]))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("user:profile", args=[username]))










# Create your views here.
