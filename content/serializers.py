from rest_framework import serializers

from content.models import Comment, Like, Post, Image


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "content", "post", "author", "created_at")


class CreateImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id", "image")


class CreateLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("id", "user", "post")


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id", "image")


class PostSerializer(serializers.ModelSerializer):
    images = CreateImageSerializer(many=True)

    class Meta:
        model = Post
        fields = ("id", "title", "content", "images", "author", "created_at")

    def create(self, validated_data):
        images_data = validated_data.pop("images", [])
        post = Post.objects.create(**validated_data)

        for image_data in images_data:
            Image.objects.create(post=post, **image_data)

        return post

    def update(self, instance, validated_data):
        images_data = validated_data.pop("images", [])
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.author = validated_data.get("author", instance.author)

        instance.images.clear()
        for image_data in images_data:
            image, created = Image.objects.get_or_create(image=image_data["image"])
            instance.images.add(image)
        instance.save()
        return instance


class PostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    likes = CreateLikeSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "created_at",
            "likes",
            "comments",

        )


class PostListSerializer(serializers.ModelSerializer):
    comments = serializers.IntegerField(source="comments.count")
    likes = serializers.IntegerField(source="likes.count")
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "content", "author", "likes", "comments")
