from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class CreaterDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30, default='')
    email = models.CharField(max_length=30)
    website_link = models.CharField(max_length=30)
    tech_stack = models.TextField()

    def __str__(self):
        return self.username
