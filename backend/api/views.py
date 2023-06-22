from django.shortcuts import render, HttpResponse
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.


class ReactView(APIView):
    def get(self, request):
        output = [{"firstname": output.firstname,
                   "lastname": output.lastname,
                   "email": output.email,
                   "website_link": output.website_link,
                   "description": output.description
                   }
                  for output in CreaterDetails.objects.all()
                  ]
        return Response(output)

    def post(self, request):
        serializer = CreatorDetailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
#
# @api_view(['GET', 'POST'])
# def creator_list(request):
#     if request.method == 'GET':
#         creators = CreaterDetails.objects.all()
#         serializer = CreatorDetailSerializer(creators, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = CreatorDetailSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def single_creator(request, pk):
#     try:
#         creator = CreaterDetails.objects.get(pk=pk)
#
#     except CreaterDetails.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = CreatorDetailSerializer(creator)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = CreatorDetailSerializer(creator, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         creator.delete()
#         return Response(status=status.HTTP_205_RESET_CONTENT)
