import factory
import pytest

from finance_advisor.advisee.models import Advisee


class AdviseeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Advisee
        django_get_or_create = ("email",)


@pytest.fixture
def mock_advisee_user():
    advisee = AdviseeFactory(email="fake_advisee@email.com")
    advisee.set_password("test_password")
    return advisee
