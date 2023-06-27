from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import *
from django.contrib.auth import get_user_model, authenticate

UserModel = get_user_model()


class CreatorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email', 'username']


class CreatorDetailLoginSerializer(serializers.ModelSerializer):
    class Meta:
        email = serializers.EmailField()
        password = serializers.CharField()

    def check_user(self, clean_data):
        user = authenticate(username=clean_data['email'], password=clean_data['password'])
        if not user:
            raise ValidationError('user not found')
        return user


class CreatorDetailRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['__all__']
