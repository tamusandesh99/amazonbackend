
from django.contrib import admin
from django.urls import path, include, re_path
from .views import *


urlpatterns = [
    path('register', UserRegister.as_view(), name='register'),
    path('login', UserLogin.as_view(), name='login'),
    path('logout', UserLogout.as_view(), name='logout'),
    path('account', UserView.as_view(), name='user'),
    path('csrfCookie', GetCSRFToken.as_view())
]
