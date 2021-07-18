from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()


class IsAdviseeFilteredByUrlSelf(BasePermission):
    """
    Check if given URL like advisee/123/goals/ is of advisee that is currently logged in.
    """

    def has_permission(self, request, view):
        advisee_id = view.kwargs["advisee_id"]
        if request.user.id is advisee_id:
            return True
        return False


class IsOwnedBySelf(BasePermission):
    """
    Check if given object, like goal, income, etc is of an advisee that is currently logged in.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if obj.owner_id is request.user.id:
                return True
            return False
        return False
