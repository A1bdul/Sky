from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone


# Create your models here.


class Photo(models.Model):
    baseurl = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    date_uploaded = models.DateTimeField(auto_now=True)
    owner = models.CharField(max_length=20)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    caption = models.CharField(max_length=140, default="")
    tags = models.IntegerField(default=0)
    main_colour = models.CharField(max_length=15, default="")

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-id']

    def total_likes(self):
        return self.likes.count


class Post:
    owner = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def total_likes(self):
        return self.likes.count


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.CharField(max_length=100)



class Comment(models.Model):
    post = models.ForeignKey(Photo, on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.post.id, str(self.user.username))


class Followers(models.Model):
    user = models.CharField(max_length=20, default="")
    follower = models.CharField(max_length=20, default="")
