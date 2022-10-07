
from django.urls import path
from .views import index, Register, Login, Logout, Chat, Trending, test, PostCreate,comment, PostEdit, DetailPost, AddLike
from user_profile.views import UserProfile


app_name='post'
urlpatterns = [
    path('', index, name='home'),
    path('<username>/', UserProfile, name='profile'),
    path('register/', Register, name='register'),
    path('login/', Login, name='login'),
    path('logout/', Logout, name='logout'),
    path('chat/', Chat, name='chat'),
    path('trending/', Trending, name='trending'),
    path('test/', test, name='test'),
    # POST
    path('create/', PostCreate, name='create'),
    path('edit/<str:id>/', PostEdit, name='edit'),
    path('detail/<str:id>/', DetailPost, name='detail'),
    path('post/<str:id>/like/', AddLike, name='like'),
    path('post/<str:id>/comment/', comment, name='comment'),

   



]