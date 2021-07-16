from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

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
