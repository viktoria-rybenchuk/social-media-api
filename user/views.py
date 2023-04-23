from django.contrib.auth import get_user_model
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import Following, Follower
from user.permissions import IsOwnerOrReadOnly
from user.serializers import (
    UserListSerializer,
    UserDetailSerializer,
    UserSerializer,
    ProfileImageSerializer,
    FollowersSerializer,
    LogoutSerializer
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,)

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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "username",
                type=OpenApiTypes.INT,
                description="Filter by movie username",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        request=ProfileImageSerializer,
        responses={200: UserSerializer},
        methods=["POST"]
    )
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

    @action(detail=True, methods=["POST"], permission_classes=(IsAuthenticated,))
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()
        username = user_to_follow.username
        user = request.user
        if not Following.objects.filter(user=user, following_user=user_to_follow).exists():
            Following.objects.create(user=user, following_user=user_to_follow)
            Follower.objects.create(user=user_to_follow, following_user=user)
            return Response(status=status.HTTP_200_OK)
        return Response(f"You have already follow {username}", status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["POST"], permission_classes=(IsAuthenticated,))
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
