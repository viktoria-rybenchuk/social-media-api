from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id or request.method in SAFE_METHODS

class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            obj.author.id == request.user.id
            or request.method in SAFE_METHODS
        )