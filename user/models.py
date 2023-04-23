from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import AUTH_USER_MODEL


class User(AbstractUser):
    profile_image = models.ImageField(upload_to="profile_images", null=True, blank=True)
    biography = models.CharField(max_length=500, blank=True)

    def __str__(self) -> str:
        return (
            f"{self.username} "
            f"({self.first_name}"
            f" {self.last_name})"
        )


class UserFollowing(models.Model):
    following = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name="following",
        on_delete=models.CASCADE
    )
    followers = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name="followers",
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (
            f"Followers: {self.followers.username}"
            f"Following: {self.followers.username}"
        )

    class Meta:
        unique_together = ("following", "followers")