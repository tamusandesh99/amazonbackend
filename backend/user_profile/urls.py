from django.urls import path
from .views import *

urlpatterns = [
    path('user', GetUserProfileView.as_view()),
    path('update', UpdateUserProfileView.as_view()),
    path('get_posts', GetUserProfileAndPostsView().as_view()),
    # path('posts', PostViewSet.as_view({'post': 'create'}), name='post-create'),
    path('post/create', CreatePostView.as_view(), name='create_post'),
]
