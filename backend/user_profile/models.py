from django.db import models

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website_link = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.website_link
