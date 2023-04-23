from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from content.models import Post, Comment
from content.serializers import (
    PostSerializer,
    PostListSerializer,
    CommentSerializer, CreateLikeSerializer, PostDetailSerializer
)
from user.permissions import IsOwnerOrReadOnly, IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer
        if self.action == "list":
            return PostListSerializer
        if self.action == "add_like":
            return CreateLikeSerializer
        return self.serializer_class

    # def get_queryset(self):
    #     following = self.request.user.following.prefetch_related(
    #         "following__id").values_list("id")
    #     return self.queryset.filter(author_id__in=following)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["POST", "GET"])
    def add_like(self, request, pk):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data={
                "post": self.get_object().id,
                "user": self.request.user.id
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


def remove_like(self, request, pk):
    post = self.get_object()
    like = post.likes.filter(user=request.user).first()

    if like is not None:
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
