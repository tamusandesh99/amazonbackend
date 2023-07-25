from django.urls import path
from .views import *

urlpatterns = [
    path('user', GetUserProfileView.as_view()),
    path('update', UpdateUserProfileView.as_view()),
    path('get_posts', GetUserProfileAndWebsiteView().as_view()),
]
