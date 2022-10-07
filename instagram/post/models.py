from django.urls import reverse
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
import uuid

def user_dir_path(instence,filename):
    return 'user_{0}/{1}'.format(instence.user.id,filename)


class Tag(models.Model):
    title   = models.CharField(max_length=100,verbose_name="Tag")
    slug    = models.SlugField(null=False,unique=True,default=uuid.uuid1)
    class Meta:
        verbose_name        = "Tag"
        verbose_name_plural = "Tags"

    def get_absolute_url(self):
        return reverse('tags', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug - slugify(self.slug)
        return super().save(*args,**kwargs)


class Post(models.Model):
    id          = models.UUIDField(primary_key=True,default=uuid.uuid4)
    picture     = models.ImageField(upload_to=user_dir_path, blank=True, null=True, verbose_name="Picture")
    caption     = models.CharField(max_length=1000, verbose_name="Caption")
    user        = models.ForeignKey(User, null=False,on_delete=models.CASCADE)
    tag         = models.ManyToManyField(Tag, related_name="tags")
    likes       = models.ManyToManyField(User,blank=True, related_name="likes")
    posted      = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('post-details', args=[str(self.id)])
    def __str__(self):
        return self.caption+' | '+self.user.username


class Follow(models.Model):
    follower    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following   = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    def __str__(self):
        return self.follower.username

class Stream(models.Model): 
    following   = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stream_following")
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stream_user")
    post        = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    date        = models.DateTimeField()

    def add_post(sender, instance, *args, **kwargs):
        post        = instance
        user        = post.user
        followers   = Follow.objects.all().filter(following=user)
        for follower in followers:
            stream  =Stream(post=post, user=follower.follower, date=post.posted, following=user)
            stream.save()  
    def __str__(self):
        return self.following.username+ ' | ' +self.post.caption
post_save.connect(Stream.add_post, sender=Post)

class Commenter(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    post    = models.ForeignKey(Post, on_delete=models.CASCADE)
    body    = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.body
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liker")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked")


