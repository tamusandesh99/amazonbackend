from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('user', GetUserProfileView.as_view()),
    path('update', UpdateUserProfileView.as_view()),
    path('get_posts', GetUserProfileAndPostsView().as_view()),
    path('post/create', CreatePostView.as_view(), name='create_post'),
    path('post/sorting/<str:sorting_style>/', SortingPosts.as_view(), name='sorting_posts'),
    # path('post/<String:title>/', DynamicPostSearch.as_view(), name='create_post'),
    re_path(r'^posts/(?P<title>[-\w]+)/$', DynamicPostSearch.as_view(), name='post_detail'),
]
