from django.shortcuts import render, HttpResponse

# Create your views here.


def Index(request):
    return HttpResponse("This is it")
