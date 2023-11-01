from django.urls import path
from posts.views.front import PostCreateView, post_list

urlpatterns = [
    path("", post_list, name="post_list"),
    path("create/", PostCreateView.as_view(), name="post_create"),
]
