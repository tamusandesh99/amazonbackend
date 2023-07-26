from django.shortcuts import render
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserProfileSerializer


class GetUserProfileView(APIView):
    def get(self, request, format=None):
        try:
            user = self.request.user
            username = user.username
            print(user)
            user_profile = UserProfile.objects.get(user=user)
            user_profile = UserProfileSerializer(user_profile)

            return Response({'profile': user_profile.data, 'username': str(username)})
        except:
            return Response({'error': 'Something went wrong when retrieving profile'})


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


class GetUserProfileAndWebsiteView(APIView):
    def get(self, request, format=None):
        try:
            user_profiles = UserProfile.objects.all()
            user_profiles_data = []
            for profile in user_profiles:
                username = profile.user.username
                website_link = profile.website_link if profile.website_link else " "
                user_profiles_data.append({'username': username, 'website_link': website_link})

            return Response({'user_profiles': user_profiles_data})
        except:
            return Response({'error': 'Something went wrong when retrieving profiles'})