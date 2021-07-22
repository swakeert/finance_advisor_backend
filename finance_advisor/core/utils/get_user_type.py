from enum import Enum

from django.contrib.auth import get_user_model

from finance_advisor.core.models import CustomUser

User = get_user_model()


class USER_TYPE_ENUM(Enum):
    ADVISEE = "advisee"
    ADVISOR = "advisor"


def get_user_type(user):
    try:
        if user.customuser.advisor:
            return USER_TYPE_ENUM.ADVISOR.value
    except CustomUser.advisor.RelatedObjectDoesNotExist:
        if user.customuser.advisee:
            return USER_TYPE_ENUM.ADVISEE.value
    return None
