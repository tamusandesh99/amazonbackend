from django.db import models


# Create your models here.


class CreaterDetails(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30, default='')
    email = models.CharField(max_length=30)
    website_link = models.CharField(max_length=30)
    tech_stack = models.TextField()

    def __str__(self):
        return self.username
