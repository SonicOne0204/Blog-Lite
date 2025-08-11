from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from django.db.models import F

from .models import User, Post, SubPost, Like, View
from .serializers import UserRegistrationSerializer, PostSerializer, SubPostSerializer
from .pagination import Pagination


@api_view(["POST"])
def like_post(request, pk):
    try:
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Login required"}, status=status.HTTP_401_UNAUTHORIZED
            )
        post = Post.objects.get(pk=pk)
        user = request.user
        like_exists = Like.objects.filter(user=request.user, post=post)
        if like_exists:
            return Response({"detail": "You already liked this post"}, status=400)
        Like.objects.create(user=user, post=post)
    except Post.DoesNotExist:
        return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    post.likes += 1
    post.save()
    return Response({"likes": post.likes}, status=status.HTTP_200_OK)


@api_view(["POST"])
def view_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    if not request.user.is_authenticated:
        return Response(
            {"detail": "Login required"}, status=status.HTTP_401_UNAUTHORIZED
        )
    with transaction.atomic():
        view, created = View.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response(
                {"detail": "You already viewed this post"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Post.objects.filter(pk=post.pk).update(views_count=F("views_count") + 1)

    return Response({"detail": "View counted successfully"}, status=status.HTTP_200_OK)


class RegitrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = Pagination

    def post(self, request, *args, **kwargs):
        """
        To create at once (bulk create), send a JSON array of post objects:
        ```json
            [
                {
                "title": "Post 1",
                "body": "Content for post 1",
                "subposts": []
                },
                {
                "title": "Post 2",
                "body": "Content for post 2",
                "subposts": [
                    {
                    "title": "Subpost 2.1",
                    "body": "Content for subpost 2.1"
                    }
                ]
                }
            ]
        ```
        """
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class SubPostListCreateAPIView(generics.ListCreateAPIView):
    queryset = SubPost.objects.all()
    serializer_class = SubPostSerializer
    pagination_class = Pagination


class SubPostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubPost.objects.all()
    serializer_class = SubPostSerializer
