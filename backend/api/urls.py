

from django.urls import path
from .views import creator_list, single_creator


urlpatterns = [
    path('creators/', creator_list),
    path('creators/<int:pk>/', single_creator)
]
