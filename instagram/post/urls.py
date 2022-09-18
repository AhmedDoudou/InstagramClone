
from django.urls import path
from .views import *


app_name='post'
urlpatterns = [
    path('', index, name='home'),
    path('profile/<int:id>/', Profile, name='profile'),
    path('register/', Register, name='register'),
    path('login/', Login, name='login'),
    path('logout/', Logout, name='logout'),
    path('chat/', Chat, name='chat'),
    path('trending/', Trending, name='trending'),





]