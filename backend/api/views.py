from django.shortcuts import render, HttpResponse
from django.utils.decorators import method_decorator
from rest_framework.authentication import SessionAuthentication

from .models import *
from .serializers import *
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from .validations import *
from .serializers import *

# Create your views here.


class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = CreatorDetailRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = (permissions.AllowAny, )
    authentication_classes = (SessionAuthentication, )

    def post(self, request):
        data = request.data
        assert validate_email(data)
        assert validate_username(data)
        assert validate_password(data)

        serializer = CreatorDetailLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
    def post (self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (SessionAuthentication, )

    def get(self, request):
        serializer = CreatorDetailSerializer(request.user)
        return Response({'self': serializer.data}, status=status.HTTP_200_OK)
    # queryset = CreaterDetails.objects.all()
    # serializer_class = CreatorDetailSerializer
    #
    # def get(self, request):
    #     firstname = request.query_params.get('firstname')
    #     email = request.query_params.get('email')
    #
    #     creators = CreaterDetails.objects.all()
    #
    #     if firstname:
    #         creators = creators.filter(firstname=firstname)
    #
    #     if email:
    #         creators = creators.filter(email=email)
    #     output = [{"id": output.id,
    #                "username": output.username,
    #                "password": output.password,
    #                "email": output.email,
    #                "website_link": output.website_link,
    #                "tech_stack": output.tech_stack
    #                }
    #               for output in creators
    #               ]
    #     return Response(output)
    #
    # def post(self, request):
    #     serializer = CreatorDetailSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data)
    #
    # def put(self, request, pk):
    #     creator = self.get_object(pk)
    #     serializer = CreatorDetailSerializer(creator, data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, pk):
    #     creator = self.get_object(pk)
    #     creator.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #
    # def get_object(self, pk):
    #     try:
    #         return CreaterDetails.objects.get(pk=pk)
    #     except CreaterDetails.DoesNotExist:
    #         raise CreaterDetails.DoesNotExist(f"Creator with ID {pk} does not exist.")


class ReactDetailView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = CreaterDetails.objects.all()
    serializer_class = CreatorDetailSerializer


class ReactLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        users = User.objects.all()
        # Check if both username and password are provided
        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = authenticate(username=username, password=password)

        # Check if authentication is successful
        if user is not None:
            login(request, user)
            # Perform any additional actions upon successful login, such as generating a token or session
            return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
