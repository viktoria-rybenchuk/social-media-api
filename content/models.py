from django.db import models

from config.settings import AUTH_USER_MODEL


class Image(models.Model):
    image = models.ImageField(
        upload_to="post_images",
        null=True,
        blank=True
    )


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    images = models.ManyToManyField(
        Image,
        related_name="posts",
        blank=True
    )

    class Meta:
        ordering = ("created_at",)

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self) -> str:
        return self.content


class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    class Meta:
        unique_together = ("post", "user")

    def __str__(self) -> str:
        return f"{self.user.username} liked {self.post.title}"


class Tag(models.Model):
    title = models.CharField(max_length=60)
    posts = models.ManyToManyField(Post, related_name="tags")
