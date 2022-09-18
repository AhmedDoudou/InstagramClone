from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User,null=False,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profiles", blank=True, null=True)
    
    def __str__(self):
        return self.user.username