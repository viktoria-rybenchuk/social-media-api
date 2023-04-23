from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from content.serializers import PostDetailSerializer
from rest_framework import serializers, exceptions
from django.utils.translation import gettext as _


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()

        except TokenError as ex:
            raise exceptions.AuthenticationFailed(ex)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_staff"
        )
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={
        "input_type": "password"}
    )

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_active:
                    msg = _("User account is disabled.")
                    raise exceptions.ValidationError(msg)
            else:
                msg = _("Unable to log in with provided credentials.")
                raise exceptions.ValidationError(msg)
        else:
            msg = _("Must include 'email' and 'password'.")
            raise exceptions.ValidationError(msg)

        data["user"] = user
        return data


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "profile_image",
            "first_name",
            "last_name",
            "email"
        )


class UserDetailSerializer(serializers.ModelSerializer):
    posts = PostDetailSerializer(many=True)
    followers = serializers.IntegerField(source="followers.count")
    following = serializers.IntegerField(source="following.count")

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "profile_image",
            "first_name",
            "last_name",
            "followers",
            "following",
            "posts",

        )


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "profile_image")


class FollowersSerializer(serializers.Serializer):
    following_user = UserListSerializer(read_only=True)
