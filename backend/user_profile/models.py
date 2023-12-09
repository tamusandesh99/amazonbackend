from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    images = ArrayField(models.TextField(), blank=True, default=list, null=True)
    links = ArrayField(models.URLField(), default=list, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)  # Initialize likes as 0
    comments = ArrayField(models.CharField(max_length=255), default=list, blank=True)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post, blank=True)

    def __str__(self):
        return self.user.username
