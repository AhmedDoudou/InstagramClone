
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
    # POST
    path('create/', PostCreate, name='create'),
    path('edit/<str:id>/', PostEdit, name='edit'),
    path('detail/<str:id>/', DetailPost, name='detail'),
    path('post/<str:id>/like', AddLike, name='like'),



    






]