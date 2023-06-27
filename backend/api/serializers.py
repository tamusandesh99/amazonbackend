from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model, authenticate

UserModel = get_user_model()


class CreatorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreaterDetails
        fields = ['id', 'username', 'password', 'email', 'website_link', 'tech_stack']


class CreatorDetailLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreaterDetails
        fields = ['id', 'username', 'password', 'email', 'website_link', 'tech_stack']


class CreatorDetailRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['__all__']

