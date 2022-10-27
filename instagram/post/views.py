from imp import reload
from xml.etree.ElementTree import Comment
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CommentForm,  PostForm, AccountForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Commenter, Follow, Post,Stream, Tag, Like
from user_profile.models import Profile, UserComment
import json
from django.http import HttpResponseBadRequest, JsonResponse
# Create your views here.
@login_required(login_url='post:login')
def index(request):
    user        = request.user
    posts       = Stream.objects.all().filter(user=user)
    comments    = UserComment.objects.all()
    profile_pics = Profile.objects.all()
    group_ids   = []
    for post in posts:
        group_ids.append(post.post_id)
    post_iteams = Post.objects.filter(id__in=group_ids).all().order_by('-posted')
    context = { 
        "post_iteams":post_iteams,
        'comments':comments,
        'profile_pics':profile_pics,

         }
    return render(request, "feed.html",context)

@login_required(login_url='post:login')
def UserProfile(request,id):
    user        = User.objects.get(id=id)
    users       = User.objects.all()
    post        = Post.objects.all().filter(user=user).count()
    my_posts    = Post.objects.all().filter(user=user).order_by("-posted")
    following   = Follow.objects.all().filter(following=user)
    follower    = Follow.objects.all().filter(follower=user)
    context = {
        "user":user,
        "users":users,
        "post":post,
        "my_posts":my_posts,
        "follower":follower,
        "following":following,
    }
    return render(request,'profile.html', context)
@login_required(login_url='post:login')  
def Chat(request):
    return render(request,"chat.html")

# def Register(request):
#     if request.user.is_authenticated:
#         return redirect('post:home')
#     else:
#         form = UserCreationForm()
#         if request.method=='POST':
#             form = UserCreationForm(request.POST)
#             if form.is_valid():
#                 form.save
#                 return redirect("post:login")
#             else:
#                 messages.error(request, 'Invalid User form')
#         context = {"form":form}
#         return render(request,"register.html",context)

def CreatAccount(request):
    form = AccountForm()
    if request.method =="POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request, "Registration successful." )
            return redirect("post:login")
        else:
            messages.error(request, "Form Invalid" )
    context = {"form":form}
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

def post(request,id):
    user = request.user
    post =Post.objects.get(id=id)
    if request.method=="POST":
        comment= Comment.objects.create(user= user,post=post,body=request.POST.get("comment"))
        comment.save()
    context = {"comment":comment}
    next = request.POST.get('next','/')   
    return HttpResponseRedirect(next,context)  

def DetailPost(request,id):
    user = request.user
    post = Post.objects.get(id=id)
    comments = Commenter.objects.filter(post=post).order_by('-created')
    form = CommentForm()
    if request.method=='POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            comm = form.save()
            comm.user = request.user
            comm.post = Post.objects.get(id=id)
            comm.save()
            return HttpResponseRedirect(reverse("post:home"), args=[id])
        else:
            form = CommentForm()
    context = {"post":post,'comments':comments}
    return render(request, "post/detail.html",context)

def AddLike(request,id):
    user = request.user                                  # user who wanna like or dislike
    post = Post.objects.get(id=id)   
    is_like = False
    for like in post.likes.all():
          if like == user :
            is_like = True  
            break
    if not is_like:
        post.likes.add(user)
    if is_like:
        post.likes.remove(user)     

    next = request.POST.get('next','/')   
    return HttpResponseRedirect(next)  

def comment(request,id):
    user        = request.user # get user 
    post        = Post.objects.get(id=id)
    comments    = UserComment.objects.all()
    if request.method=="POST":
        body    = request.POST.get("body")
        comment = UserComment.objects.create(user=user,post=post,body=body)
        comment.save()
        return redirect("post:home")
    context = {
        "post":post,
        "comments":comments
    }
    return render(request, "feed.html",context)

    
def test(request):
    user = request.user
    post = Post.objects.filter(user=user)
    return render(request,"test.html",{"post":post})

def Posts(request):
    # request.is_ajax() is deprecated since django 3.1
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'GET':
            posts = list(Post.objects.all().values())
            return JsonResponse({'context': posts})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')

# def AddComment(request,id):
#     user = request.user.id
#     post = Post.objects.get(id=id)
#     comments = Commenter.objects.filter(post=post,user=user).order_by('-created')
#     form = CommentForm()
#     if request.method=='POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             form.save
#             return HttpResponseRedirect(request.path_info)
#     context={"comments":comments}
#     return render(request, "user/test.html",context)

# @login_required(login_url='base:login')
# def room(request,pk):
#     room = Room.objects.get(id=pk)
#     participants = room.participants.all()
#     room_messages = room.message_set.all().order_by('-created')
#     if request.method =="POST":
#         message = Message.objects.create(
#             user=request.user,
#             room = room,
#             body = request.POST.get("body")
#         )
#         room.participants.add(request.user)
#         return redirect("base:room", room.id)
#     context = {'room':room,'room_messages':room_messages,'participants':participants}
#     return render(request,'room/room.html', context)




# def Register(request):
#     if request.method=="POST":
#         user_email = request.POST["email"]
#         user_name = request.POST["username"]
#         user_pass = request.POST["password"]
#         try:
#             user_obj = User.objects.create(username=user_name,email=user_email,password=user_pass)
#             user_obj.set_password(user_pass)
#             user_obj.save()
#             user_auth = authenticate(username=user_name,password=user_pass)
#             login(request,user_auth)
#             return redirect('post:home')

#         except:
#             messages.add_message(request,messages.ERROR,'can not sign up')
#             return render(request,'register.html')
#     return render(request,'register.html')






# post        = Post.objects.all().filter(user=user).count()
    # followers   = Follow.objects.all().filter(follower=user)
    # my_posts    = Post.objects.all().filter(user=user).order_by("-posted")
    # follower    = Follow.objects.all().filter(follower=user).count()
    # following   = Follow.objects.all().filter(following=user).count()

























































































