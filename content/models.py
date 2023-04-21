from django.db import models

from config.settings import AUTH_USER_MODEL


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="post_images", null=True, blank=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes")

    def __str__(self) -> str:
        return f"{self.user.username} liked {self.post.title}"
