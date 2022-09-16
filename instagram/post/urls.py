
from django.urls import path
from .views import *


app_name='post'
urlpatterns = [
    path('', index, name='home'),
    path('register/', Register, name='register'),
    path('login/', Login, name='login'),


]