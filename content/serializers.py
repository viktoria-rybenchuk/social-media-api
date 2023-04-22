from rest_framework import serializers

from content.models import Comment, Like, Post, Image


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Comment
        fields = ("id", "content", "author", "created_at")
class CreateImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id", "image")

class CreateLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("id", "user", "post")

class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "author", "post", "content")

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id", "image")


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")
    comments = CommentSerializer(many=True)
    images = serializers.SlugRelatedField(many=True, slug_field="image", read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "content", "images", "author", "created_at", "comments")

class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")
    comments = CreateCommentSerializer(many=True)
    likes = CreateLikeSerializer(many=True)
    images = PostImageSerializer(many=True)

    class Meta:
        model = Post
        fields = ("id", "title", "content", "images", "author", "created_at", "comments", "likes")

