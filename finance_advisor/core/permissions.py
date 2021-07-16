from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

User = get_user_model()


class IsSafeRequest(BasePermission):
    """
    Permission to check if request is GET, HEAD or OPTIONS.
    """

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


class IsSelf(BasePermission):
    """
    Permission to check if currently authenticated user is trying to access their own profile.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.id is obj.id:
            return True
        return False
