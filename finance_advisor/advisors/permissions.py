from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

from finance_advisor.core.models import CustomUser

User = get_user_model()


class IsClient(BasePermission):
    """
    Check if given object of advisee is a client of currently authenticated advisor user.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            try:
                if obj in request.user.customuser.advisor.clients.all():
                    return True
            except (
                User.customuser.RelatedObjectDoesNotExist,
                CustomUser.advisor.RelatedObjectDoesNotExist,
            ):
                return False
        return False


class IsAdviseeFilteredByUrlClient(BasePermission):
    """
    Check if given URL like advisee/123/goals/ is of an advisee that is a client of currently authenticated advisor user.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            advisee_id = view.kwargs.get("advisee_id")
            try:
                clients = request.user.customuser.advisor.clients.all().values_list(
                    "id",
                    flat=True,
                )
                if advisee_id in clients:
                    return True
            except (
                User.customuser.RelatedObjectDoesNotExist,
                CustomUser.advisor.RelatedObjectDoesNotExist,
            ):
                return False
        return False


class IsOwnedByClient(BasePermission):
    """
    Check if given object, like goal, income, etc is of an advisee that is a client of currently authenticated advisor user.
    """

    def has_object_permission(self, request, view, obj):

        if request.user.is_authenticated:
            try:
                if obj.owner in request.user.customuser.advisor.clients.all():
                    return True
            except (
                User.customuser.RelatedObjectDoesNotExist,
                CustomUser.advisor.RelatedObjectDoesNotExist,
            ):
                return False
        return False
