from django.urls import path
from .views import *


app_name='message'
urlpatterns = [
     # MESSAGES
    path('chat/', NewMessage, name='chat'),
    # path('<username>/follow/<option>', FollowAction, name='follow'),
    # path('<username>/edit/', EditProfile, name='edit_profile'),
    # path('<username>/<str:id>/', comment, name='comment'),

]