from django.shortcuts import render, HttpResponse
from .models import CreaterDetails
from .serializers import CreatorDetailSerializer
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


@api_view(['GET', 'POST'])
def creator_list(request):
    if request.method == 'GET':
        creators = CreaterDetails.objects.all()
        serializer = CreatorDetailSerializer(creators, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CreatorDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def single_creator(request, pk):
    try:
        creator = CreaterDetails.objects.get(pk=pk)

    except CreaterDetails.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CreatorDetailSerializer(creator)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CreatorDetailSerializer(creator, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        creator.delete()
        return Response(status=status.HTTP_205_RESET_CONTENT)
