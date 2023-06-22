from rest_framework import serializers
from .models import AuthorDetails


class AuthorDetailSerializer(serializers.Serializer):
    firstname = serializers.CharField(max_length=30)
    lastname = serializers.CharField(max_length=30)
    email = serializers.CharField(max_length=30)
    website_link = serializers.CharField(max_length=30)
    description = serializers.CharField()

    def create(self, validated_data):
        return AuthorDetails.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.email = validated_data.get('email', instance.email)
        instance.website_link = validated_data.get('website_link', instance.website_link)
        instance.description = validated_data.get('description', instance.description)
