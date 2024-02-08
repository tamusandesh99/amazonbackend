from rest_framework import serializers
from .models import UserProfile, Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'images', 'links', 'likes', 'comments', 'timestamp', 'username']

    def create(self, validated_data):
        user_profile = self.context['request'].user.userprofile  # Get the user profile from the view context
        post = Post.objects.create(user_profile=user_profile, **validated_data)
        return post


class UserProfileSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
