from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import AUTH_USER_MODEL
from content.models import Image


class User(AbstractUser):
    profile_image = models.ImageField(upload_to="profile_images", null=True, blank=True)
    biography = models.CharField(max_length=500, blank=True)

    def __str__(self) -> str:
        return (
            f"{self.username} "
            f"({self.first_name}"
            f" {self.last_name})"
        )
class Follower(models.Model):
    following_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="followers",
        on_delete=models.CASCADE,
        null=True,
        default=""
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="following",
        on_delete=models.CASCADE,
        null=True,
        default=""
    )
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("user", "following_user")

    def __str__(self) -> str:
        return f"{self.following_user.username} follows {self.user.username}"

class Following(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="following_users",
        on_delete=models.CASCADE,
        null=True,
        default=""
    )
    following_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="followings",
        on_delete=models.CASCADE,
        null=True,
        default=""
    )
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("user", "following_user")

    def __str__(self) -> str:
        return f"{self.user.username} follows {self.following_user.username}"
