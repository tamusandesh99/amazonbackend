from rest_framework.authentication import SessionAuthentication
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from .validations import *
from .serializers import *


# Create your views here.


@method_decorator(csrf_protect, name='dispatch')
class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        clean_data = custom_validation(request.data)
        print(clean_data)
        serializer = CreatorDetailRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(clean_data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_protect, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        return Response({'Success: CSRF cookie set'})


@method_decorator(csrf_protect, name='dispatch')
class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = request.data
        assert validate_email(data)
        # assert validate_username(data)
        assert validate_password(data)
        print("checks here")
        try:
            serializer = CreatorDetailLoginSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.check_user(data)
                login(request, user)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'Something went wrong'})


class UserLogout(APIView):
    def post(self, request):
        try:
            logout(request)
            return Response({'success: Logged Out'}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Something went wrong when logging out'})


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        serializer = CreatorDetailSerializer(request.user)
        return Response({'self': serializer.data}, status=status.HTTP_200_OK)