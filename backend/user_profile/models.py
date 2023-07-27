from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=255)
    website_link = models.CharField(max_length=255)
    tech_stack = models.CharField(max_length=255)

    def __str__(self):
        return self.website_link


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post, blank=True)

    def __str__(self):
        return self.user.username
