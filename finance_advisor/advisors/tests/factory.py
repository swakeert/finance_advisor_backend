import factory
import pytest

from finance_advisor.advisees.tests.factory import AdviseeFactory, mock_advisee_user
from finance_advisor.advisors.models import (
    Advisor,
    AdvisorRelationship,
    AdvisorRelationshipBilling,
)


class AdvisorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Advisor
        django_get_or_create = ("email",)


class AdvisorRelationshipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AdvisorRelationship
        django_get_or_create = ("advisee", "advisor")

    advisee = factory.SubFactory(AdviseeFactory)
    advisor = factory.SubFactory(AdvisorFactory)


class AdvisorRelationshipBillingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AdvisorRelationshipBilling
        django_get_or_create = ("relationship",)

    relationship = factory.SubFactory(AdvisorRelationshipFactory)


@pytest.fixture
def mock_advisor_user():
    advisor = AdvisorFactory(email="fake_advisor@email.com")
    advisor.set_password("test_password")
    return advisor


@pytest.fixture
def mock_relationship(mock_advisee_user, mock_advisor_user):
    relationship = AdvisorRelationshipFactory(
        advisee=mock_advisee_user, advisor=mock_advisor_user
    )
    return relationship
