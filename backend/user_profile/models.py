from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    website_link = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.website_link
