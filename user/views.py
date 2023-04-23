from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from user.models import Following, Follower
from user.serializers import (
    UserListSerializer,
    UserDetailSerializer,
    UserSerializer,
    ProfileImageSerializer,
    FollowersSerializer,
)


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
        if self.action in ["following", "followers"]:
            return FollowersSerializer
        return self.serializer_class

    def get_queryset(self):
        username = self.request.query_params.get("username")
        queryset = self.queryset

        if username:
            queryset = queryset.filter(username__icontains=username)

        return queryset


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

    @action(detail=True, methods=["POST"])
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()
        username = user_to_follow.username
        user = request.user
        if not Following.objects.filter(user=user, following_user=user_to_follow).exists():
            Following.objects.create(user=user, following_user=user_to_follow)
            Follower.objects.create(user=user_to_follow, following_user=user)
            return Response(status=status.HTTP_200_OK)
        return Response(f"You have already follow {username}", status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["POST"])
    def unfollow(self, request, pk=None):
        user_to_unfollow = self.get_object()
        user = request.user
        Following.objects.filter(user=user, following_user=user_to_unfollow).delete()
        Follower.objects.filter(user=user_to_unfollow, following_user=user).delete()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"])
    def followers(self, request, pk):
        user = self.get_object()
        followers = Follower.objects.filter(user_id=user.id)
        serializer = self.get_serializer(followers, many=True)
        return Response(serializer.data)
    @action(detail=True, methods=["GET"])
    def following(self, request, pk=None):
        user = self.get_object()
        following_users = Following.objects.filter(user_id=user.id)
        serializer = self.get_serializer(following_users, many=True)
        return Response(serializer.data)



