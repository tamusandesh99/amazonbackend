from rest_framework import serializers
from .models import *


class CreatorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreaterDetails
        fields = ['id', 'firstname', 'lastname', 'email', 'website_link', 'description']

