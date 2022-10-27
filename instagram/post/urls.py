from django.urls import path
from .views import index, CreatAccount, Login, Logout, Chat, Trending, Posts, PostCreate,comment, PostEdit, DetailPost, AddLike
from user_profile.views import UserProfile


app_name='post'
urlpatterns = [
    path('', index, name='home'),
    path('login/', Login, name='login'),
    path('register/', CreatAccount, name='register'),
    path('logout/', Logout, name='logout'),
    # path('<username>/', UserProfile, name='profile'),
    
    path('chat/', Chat, name='chat'),
    path('trending/', Trending, name='trending'),
    path('test/', Posts, name='test'),
    # POST
    path('create/', PostCreate, name='create'),
    path('edit/<str:id>/', PostEdit, name='edit'),
    path('detail/<str:id>/', DetailPost, name='detail'),
    path('post/<str:id>/like/', AddLike, name='like'),
    path('post/<str:id>/comment/', comment, name='comment'),

   



]