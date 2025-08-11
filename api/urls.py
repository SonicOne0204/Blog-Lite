from django.urls import path
from .views import (
    like_post,
    view_post,
    RegitrationView,
    PostListCreateAPIView,
    PostRetrieveUpdateDestroyAPIView,
    SubPostListCreateAPIView,
    SubPostRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("register/", RegitrationView.as_view(), name="register"),
    path("posts/", PostListCreateAPIView.as_view(), name="post-list"),
    path(
        "posts/<int:pk>/",
        PostRetrieveUpdateDestroyAPIView.as_view(),
        name="post-detail",
    ),
    path("sub-posts/", SubPostListCreateAPIView.as_view(), name="sub-post-list"),
    path(
        "sub-posts/<int:pk>/",
        SubPostRetrieveUpdateDestroyAPIView.as_view(),
        name="sub-post-detail",
    ),
    path("posts/<int:pk>/like/", like_post, name="like-post"),
    path("posts/<int:pk>/view/", view_post, name="view-post"),
]
