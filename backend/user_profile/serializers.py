from rest_framework import serializers
from .models import UserProfile, Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'website_link', 'tech_stack']  # Replace with your desired fields

    def create(self, validated_data):
        user_profile = self.context['user_profile']  # Get the user profile from the view context
        post = Post.objects.create(user_profile=user_profile, **validated_data)
        return post


class UserProfileSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
