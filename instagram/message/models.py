from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    sender   = models.ForeignKey(User, on_delete=models.CASCADE,related_name="sender")
    reciever = models.ForeignKey(User, on_delete=models.CASCADE,related_name="reciever")
    body     = models.TextField()
    created  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body