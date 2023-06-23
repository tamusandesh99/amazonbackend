
from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('creators/', ReactView.as_view(), name="blah"),
    path('creators/<int:pk>/', ReactDetailView.as_view(), name="creator-detail"),
    path('creator/search/', ReactView.as_view(), name='creator-search'),
]
