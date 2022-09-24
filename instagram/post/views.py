from turtle import title
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, PostForm
from django.contrib.auth.models import User
from .models import Follow, Post,Stream, Tag, Like
# Create your views here.
@login_required(login_url='post:login')
def index(request):
    user = request.user
    post = Post.objects.all().filter(user=user).count()
    posts  = Stream.objects.all().filter(user=user)
    my_posts = Post.objects.all().filter(user=user).order_by("-posted")
    follower = Follow.objects.all().filter(follower=user).count()
    following = Follow.objects.all().filter(following=user).count()
    group_ids = []
    for post in posts:
        group_ids.append(post.post_id)
    post_iteams = Post.objects.filter(id__in=group_ids).order_by('-posted')
    context = { 
        "posts":posts,
        "post_iteams":post_iteams,
        "follower":follower,
        "post":post,
        "follower":follower,
        "following":following,
        "my_posts":my_posts,

        }

    return render(request, "feed.html",context)

@login_required(login_url='post:login')
def Profile(request,id):
    user = User.objects.get(id=id)
    users = User.objects.all()
    post = Post.objects.all().filter(user=user).count()
    follower = Follow.objects.all().filter(follower=user).count()
    following = Follow.objects.all().filter(following=user).count()
    context = {
        "user":user,
        "users":users,
        "post":post,
        "follower":follower,
        "following":following,
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

def PostCreate(request):
    user = request.user.id
    tag_obj = []
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get("picture")
            caption = form.cleaned_data.get("caption")
            tag_form = form.cleaned_data.get("tag")
            tag_list = list(tag_form.split(','))
            for tag in tag_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tag_obj.append(t)
            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user_id=user)
            p.tag.set(tag_obj)
            p.save()
            return redirect("post:home")
    else :
        form = PostForm()
        context = {"form":form}
        return render(request,"post/create.html",context)

def PostEdit(request,id):
    user = request.user.id
    tag_obj = []
    post = Post.objects.get(id=id)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get("picture")
            caption = form.cleaned_data.get("caption")
            tag_form = form.cleaned_data.get("tag")
            tag_list = list(tag_form.split(','))
            for tag in tag_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tag_obj.append(t)
            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user_id=user)
            p.tag.set(tag_obj)
            p.save()
            return redirect("post:home")
    else :
        form = PostForm(instance=post) 
        context = {"form":form}
        return render(request,"post/edit.html",context)

# def Likes(request,id):
#     user  = request.user
#     post = Post.objects.get(id=id)
#     carrent_likes = Post.likes
#     liked = Like.objects.filter(user=user,post=post).count()
#     if not liked:
#         liked = Like.objects.create(user=user, post=post)
#         carrent_likes=+1
#     else:
#         liked = Like.objects.filter(user=user, post=post).delete()
#         carrent_likes-=1
#     post.likes= carrent_likes
#     post.save()

#     context = {}
#     return render(request,"")

def DetailPost(request,id):
    user = request.user
    post = Post.objects.get(id=id)
    context = {"post":post}
    return render(request, "post/detail.html",context)

def AddLike(request,id):
    user = request.user
    post = Post.objects.get(id=id)
    likes = post.likes
    carent_likes = Post.objects.filter(likes=likes).count()
    print(carent_likes)
    # if request.method == "POST":
    #     likes = Like.objects.add(user=user,post=post)
    #     post.likes+=1
    return HttpResponseRedirect("")