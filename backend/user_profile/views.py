from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.generics import CreateAPIView

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

            # Create a new post and set the user to the currently logged-in user
            post = Post.objects.create(
                title=data['title'],
                website_link=data['website_link'],
                tech_stack=data['tech_stack'],
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


