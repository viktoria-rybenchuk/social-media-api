from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from content.serializers import PostCreateSerializer
from user.models import UserFollowing
from user.serializers import UserListSerializer, UserDetailSerializer, UserSerializer, ProfileImageSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        if self.action == "list":
            return UserListSerializer
        if self.action == "upload_profile_image":
            return ProfileImageSerializer
        if self.action == "add_post":
            return PostCreateSerializer

        return self.serializer_class

    def get_queryset(self):
        username = self.request.query_params.get("username")
        queryset = self.queryset

        if username:
            queryset = queryset.filter(username__icontains=username)

        return queryset
    @action(detail=True, methods=["GET"], url_path="following")
    def following(self, request, pk=None):
        user = self.get_object()
        following_users = user.following.all()
        serializer = UserSerializer(following_users, many=True)
        return Response(serializer.data)

    @action(
        methods=["POST", "GET"],
        detail=True,
        url_path="upload-image",
    )
    def upload_profile_image(self, request, pk=None):
        """Endpoint for uploading image to specific profile"""
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
