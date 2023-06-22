from django.db import models


# Create your models here.


class CreaterDetails(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    website_link = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.firstname
