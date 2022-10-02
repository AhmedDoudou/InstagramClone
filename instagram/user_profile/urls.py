
from django.urls import path
from .views import *


app_name='user'
urlpatterns = [
     # profile
    path('<username>/', UserProfile, name='profile'),
    path('<username>/follow/<option>', FollowAction, name='follow'),
    path('<username>/edit/', EditProfile, name='edit_profile'),


]