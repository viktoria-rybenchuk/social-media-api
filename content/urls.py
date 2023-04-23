from django.urls import path, include
from rest_framework import routers

from content.views import PostViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
router.register("posts/(?P<post_id>\d+)/comments", CommentViewSet)


app_name = "content"

urlpatterns = [
    path("", include(router.urls)),
]
