from django.http import HttpResponseRedirect
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.urls import resolve, reverse
from post.models import Post,Stream, Follow
from .models import Profile
from .forms import *
import random



def UserProfile(request,username):
    user        = get_object_or_404(User,username=username) # get user 
    profile     = Profile.objects.get(user=user)    # get user profile
    url_name    = resolve(request.path).url_name   # get the path 
    post        = Post.objects.all().filter(user=user)
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
    # Suggestions Friends
    # uf = Follow.objects.all().filter(follower=user).count()
    # suggestion_user = list(Profile.objects.all())
    # random_user = random.sample(suggestion_user, 3)
    # Suggestions Posts
    # pl = Post.objects.all().filter(user=user).count()
    # suggestion_post = list(Post.objects.all().filter(posted=timezone.now()))
    # random_post = random.sample(suggestion_post, 3)
    context = {
        'posts_paginator':posts_paginator,
        'posts':posts,
        'post':post,
        # 'random_user':random_user,
        # 'random_post':random_post,
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

def comment(request,username,id):
    user        = get_object_or_404(User,username=username) # get user 
    post        = Post.objects.get(id=id)
    comments    = UserComment.objects.filter(post=post)
    if request.method=="POST":
        body    = request.POST.get("body")
        comment = UserComment.objects.create(user=user,post=post,body=body)
        comment.save()
        return HttpResponseRedirect(request.path_info)
    context = {
        "post":post,
        "comments":comments
    }
    return render(request,"user/test.html",context)







# Create your views here.
