from django.contrib.postgres.fields import ArrayField
from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    images = ArrayField(models.ImageField(upload_to='images/'), blank=True, default=list)
    links = ArrayField(models.URLField(), blank=True, default=list)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post, blank=True)

    def __str__(self):
        return self.user.username
