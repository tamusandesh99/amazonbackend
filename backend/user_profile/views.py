from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
from rest_framework import status, viewsets, permissions
from operator import itemgetter
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserProfile, Post
from .serializers import UserProfileSerializer, PostSerializer


class GetUserProfileView(APIView):
    def get(self, request, format=None):
        try:
            user = self.request.user
            username = user.username
            user_profile = UserProfile.objects.get(user=user)
            user_profile = UserProfileSerializer(user_profile)

            return Response({'profile': user_profile.data, 'username': str(username)})

        except UserProfile.DoesNotExist:
            return Response({'error': 'UserProfile not found for the current user'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Something went wrong when retrieving profile'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateUserProfileView(APIView):
    def put(self, request, format=None):
        try:
            user = self.request.user
            username = user.username

            data = self.request.data
            website_link = data['website_link']
            user_profile = UserProfile.objects.filter(user=user).first()

            if user_profile:
                user_profile.website_link = website_link
                user_profile.save()

                # Now, retrieve the updated instance using the serializer
                serializer = UserProfileSerializer(user_profile)
                return Response({'profile': serializer.data, 'username': str(username)})
            else:
                return Response({'error': 'UserProfile not found for the current user'},
                                status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Something went wrong when updating profile'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetUserProfileAndPostsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        try:
            user_profiles = UserProfile.objects.all()
            user_profiles_data = []

            for profile in user_profiles:
                # Serialize the user profile data
                user_profile_serializer = UserProfileSerializer(profile)
                user_data = user_profile_serializer.data
                username = profile.user.username
                # Retrieve all posts of the user profile
                posts = profile.posts.all()
                # Serialize the posts data
                post_serializer = PostSerializer(posts, many=True)
                posts_data = post_serializer.data

                # Add the posts data to the user profile data
                user_data['posts'] = posts_data

                user_profiles_data.append({'username': username, 'posts': posts_data})

            return Response({'user_profiles': user_profiles_data})
        except Exception as e:
            return Response({'error': 'Something went wrong when retrieving profiles'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CreatePostView(APIView):
    def post(self, request, format=None):
        try:
            # Retrieve the current user
            user = self.request.user

            # Get the data from the request
            data = request.data
            images = data.get('images', [])
            if images is None:
                images = []

            # Create a new post and set the user to the currently logged-in user
            post = Post.objects.create(
                title=data['title'],
                description=data['description'],
                images=data['images'],
                links=data['links'],
                user_profile=user.userprofile
                # user=user  # Set the user of the post to the currently logged-in user
            )

            user.userprofile.posts.add(post)
            # Serialize the post data
            serializer = PostSerializer(post)
            # Return the serialized post data in the response
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({'error': 'Something went wrong when creating the post'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DynamicPostSearch(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, title, format=None):
        formatted_title = title.replace('_', ' ')
        post = get_object_or_404(Post, title=formatted_title)
        username = post.user_profile.user.username
        post_serializer = PostSerializer(post)
        data = {'post': post_serializer.data, 'username': username}
        return Response(data)


# comeback when sorting in backend seems reasonable
class SortingPosts(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, sorting_style=None, format=None):
        try:
            # Retrieve all posts from all user profiles
            all_posts = []
            user_profiles = UserProfile.objects.all()

            for profile in user_profiles:
                posts = profile.posts.all()
                all_posts.extend(posts)

            # Sort the combined posts based on the specified sorting style
            if sorting_style:
                all_posts = self.sort_posts(all_posts, sorting_style)

            # Create a list of dictionaries with 'username' and 'post'
            user_profiles_data = []

            for post in all_posts:
                user_profiles_data.append(
                    {'username': post.user_profile.user.username, 'post': PostSerializer(post).data})

            return Response({'Posts': user_profiles_data})
        except Exception as e:
            return Response({'error': 'Something went wrong when retrieving profiles'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def sort_posts(self, posts_data, sorting_style):
        now = timezone.now()

        if sorting_style.lower() == 'hot':
            # Customize sorting logic for 'Hot'
            # For example, based on likes and recency
            posts_data.sort(key=lambda x: (x.likes, x.timestamp), reverse=True)
        elif sorting_style.lower() == 'mostcomments':
            # Customize sorting logic for 'Most Comment'
            # For example, based on the number of comments
            posts_data.sort(key=lambda x: len(x.comments), reverse=True)
        elif sorting_style.lower() == 'mostlikes':
            # Customize sorting logic for 'Most Likes'
            # For example, based on the number of likes
            posts_data.sort(key=lambda x: x.likes, reverse=True)
        elif sorting_style.lower() == 'recent':
            posts_data.sort(key=lambda x: x.id, reverse=True)

        return posts_data
