from django.contrib.auth import get_user_model
from rest_framework import serializers

from content.serializers import PostDetailSerializer

class UserSerializer(serializers.ModelSerializer):
    posts = PostDetailSerializer(many=True)
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "biography", "posts")
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name")

class UserDetailSerializer(serializers.ModelSerializer):
    posts = PostDetailSerializer(many=True)
    class Meta:
        model = get_user_model()
        fields = ("username", "profile_image", "first_name", "last_name", "posts")

class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "profile_image")