from rest_framework import serializers
from .models import *


class CreatorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreaterDetails
        fields = ['id', 'username', 'password', 'email', 'website_link', 'tech_stack']

