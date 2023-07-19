from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model, authenticate

UserModel = get_user_model()


class CreatorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email', 'username']


class CreatorDetailLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def check_user(self, clean_data):
        username = clean_data.get('username')
        email = clean_data.get('email')
        password = clean_data['password']

        if username:
            user = authenticate(username=username, password=password)
        elif email:
            print("email")
            user = authenticate(email=email, password=password)
        else:
            raise ValidationError('Invalid credentials')

        if not user:
            raise ValidationError('User not found')
        return user


class CreatorDetailRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'

    def create(self, clean_data):
        user_obj = UserModel.objects.create_user(email=clean_data['email'], password=clean_data['password'],
                                                 username=clean_data['username'])
        user_obj.save()

        return user_obj
