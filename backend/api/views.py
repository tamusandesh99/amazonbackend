from django.middleware.csrf import get_token
from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from .validations import *
from .serializers import *
from user_profile.models import UserProfile

# Create your views here.


@method_decorator(csrf_protect, name='dispatch')
class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
                UserProfile.objects.create(user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        return Response({'Success': 'CSRF Cookie set'})


@method_decorator(csrf_protect, name='dispatch')
class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = request.data
        try:
            serializer = UserLoginSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.check_user(data)
                login(request, user)
                return Response({'success': 'User authenticated'})
        except:
            return Response({'error': 'Error Authenticating'})


class UserLogout(APIView):
    def post(self, request):
        try:
            logout(request)
            return Response({'success': 'Logged Out'})
        except:
            return Response({'error': 'Something went wrong when logging out'})


class CheckAuthenticated(APIView):
    def get(self, request, format=None):
        user = self.request.user
        try:
            isAuthenticated = user.is_authenticated
            if isAuthenticated:
                return Response({'isAuthenticated': 'success'})
            else:
                return Response({'isAuthenticated': 'error'})
        except:
            return Response({'error': 'Something went wrong'})


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response({'self': serializer.data}, status=status.HTTP_200_OK)
