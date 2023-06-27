
from django.contrib import admin
from django.urls import path, include, re_path
from .views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', ReactView.as_view(), name="blah"),
    # path('creators/', ReactView.as_view(), name="blah"),
    # path('creators/<int:pk>/', ReactDetailView.as_view(), name="creator-id"),
    # path('creator/search/', ReactView.as_view(), name='creator-search'),
    # path('creators/login/', ReactLoginView.as_view(), name="creator-login"),
    path('register', UserRegister.as_view(), name='register'),
    path('login', UserLogin.as_view(), name='login'),
    path('logout', UserLogout.as_view(), name='logout'),
    path('user', UserView.as_view(), name='user')
]
