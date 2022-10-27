from django.db import models

# Create your models here.
class Friend(models.Model):
    # NICK NAME should be unique
    nick_name = models.CharField(max_length=100, unique =  True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.nick_name