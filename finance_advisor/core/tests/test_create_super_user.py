import pytest
from django.contrib.auth import authenticate

from finance_advisor.core.management.commands.create_super_user import create_super_user


@pytest.fixture
def super_user():
    create_super_user("username", "password")


@pytest.mark.django_db
def test_does_create_super_user(super_user):
    super_user = authenticate(username="username", password="password")  # nosec

    assert super_user is not None
    assert super_user.is_superuser


@pytest.mark.django_db
def test_updates_password_if_user_exists(super_user):
    create_super_user("username", "new_password")
    super_user = authenticate(username="username", password="new_password")  # nosec
    assert super_user is not None
