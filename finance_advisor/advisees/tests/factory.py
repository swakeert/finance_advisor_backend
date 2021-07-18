import factory
import pytest
from rest_framework.test import APIClient

from finance_advisor.advisees.models import Advisee


class AdviseeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Advisee
        django_get_or_create = ("email",)


@pytest.fixture()
def mock_advisee_user():
    advisee = AdviseeFactory(email="advisee_0@email.com")
    advisee.set_password("test_password")
    return advisee


@pytest.fixture()
def mock_alternate_advisee_user():
    advisee = AdviseeFactory(email="advisee_1@email.com")
    advisee.set_password("test_password")
    return advisee


@pytest.fixture
def authenticated_api_client_as_advisee(mock_advisee_user):
    api_client = APIClient()
    api_client.force_authenticate(mock_advisee_user)
    return api_client
