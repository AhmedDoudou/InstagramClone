from django.db import models
from django.db import models
from django.contrib.auth.models import User
from post.models import Post

def user_dir_path(instence,filename):
    return 'user_{0}/{1}'.format(instence.user.id,filename)

class Profile(models.Model):
    user            = models.OneToOneField(User,on_delete=models.CASCADE, related_name="user_profile")
    first_name      = models.CharField(max_length=100, blank=True, null=True)
    last_name       = models.CharField(max_length=100, blank=True, null=True)
    location        = models.CharField(max_length=100, blank=True, null=True)
    url             = models.CharField(max_length=100, blank=True, null=True)
    bio             = models.TextField(max_length=200, blank=True, null=True)
    profile_pic = models.ImageField(upload_to=user_dir_path, blank=True, null=True, verbose_name="profile_pic")
    created     = models.DateField(auto_now_add=True)
    def __str__(self):
            return self.first_name


class UserComment(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    post    = models.ForeignKey(Post, on_delete=models.CASCADE)
    body    = models.TextField()
    created = models.DateTimeField(auto_now_add=True)













