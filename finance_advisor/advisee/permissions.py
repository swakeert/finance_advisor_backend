from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

from finance_advisor.advisee.models import Advisee
from finance_advisor.advisor.models import Advisor
from finance_advisor.core.models import CustomUser

User = get_user_model()


class AdviseePermission(BasePermission):
    """
    Advisee can view and edit self. Advisor can only view Advisees they have a relationship with.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.id is obj.id:
            return True
        try:
            if (
                obj in request.user.customuser.advisor.clients.all()
                and request.method in SAFE_METHODS
            ):
                return True
        except (
            User.customuser.RelatedObjectDoesNotExist,
            CustomUser.advisor.RelatedObjectDoesNotExist,
        ):
            return False
        return False
