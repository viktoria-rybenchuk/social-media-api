from rest_framework import serializers

from content.models import Comment, Like, Post, Image, Tag


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "content",
            "post",
            "created_at"
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "title")


class CreateImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id", "image")


class CreateLikeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        many=True,
        slug_field="username",
        read_only=True
    )

    class Meta:
        model = Like
        fields = ("id", "user")


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id", "image")


class PostSerializer(serializers.ModelSerializer):
    images = CreateImageSerializer(many=True, allow_empty=True, required=False)
    tags = TagSerializer(many=True, allow_empty=True, required=False)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "images",
            "tags",
            "created_at"
        )

    def create(self, validated_data):
        tag_data = validated_data.pop("tags", [])
        images_data = validated_data.pop("images", [])
        post = Post.objects.create(**validated_data)
        for tag in tag_data:
            Tag.objects.create(**tag)
            post.tags.add(tag)
        for image_data in images_data:
            Image.objects.create(**image_data)
            post.tags.add(image_data)

        return post

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", [])
        images_data = validated_data.pop("images", [])
        instance.title = validated_data.get(
            "title", instance.title
        )
        instance.content = validated_data.get(
            "content", instance.content
        )
        instance.author = validated_data.get(
            "author",
            instance.author
        )

        instance.images.clear()
        for image_data in images_data:
            image, created = Image.objects.get_or_create(
                image=image_data["image"]
            )
            instance.images.add(image)
        instance.save()
        instance.tags.clear()
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(
                tag=tag_data["tag"]
            )
            instance.tags.add(tag)
        instance.save()
        return instance


class PostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    likes = CreateLikeSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "created_at",
            "tags",
            "likes",
            "comments",

        )


class PostListSerializer(serializers.ModelSerializer):
    comments = serializers.IntegerField(
        source="comments.count"
    )
    likes = serializers.IntegerField(
        source="likes.count"
    )
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )
    tags = serializers.SlugRelatedField(
        slug_field="title",
        read_only=True,
        many=True
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "author",
            "tags",
            "likes",
            "comments"
        )
