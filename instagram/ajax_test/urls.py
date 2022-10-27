from django.urls import path
from .views import *


app_name='ajax'
urlpatterns = [
    path('', index, name = "home"),
    path('profiles', GetProfile, name = "getProfiles"),
    path('create', Create, name = "create"),
]