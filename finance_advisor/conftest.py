import pytest
from rest_framework.test import APIClient

from finance_advisor.advisees.tests.factory import AdviseeFactory
from finance_advisor.advisors.tests.factory import (
    AdvisorFactory,
    AdvisorRelationshipFactory,
)
from finance_advisor.core.tests.factory import CurrencyFactory


@pytest.fixture
def mock_advisee_user():
    advisee = AdviseeFactory(email="advisee_0@email.com")
    return advisee


@pytest.fixture
def mock_alternate_advisee_user():
    advisee = AdviseeFactory(email="advisee_1@email.com")
    return advisee


@pytest.fixture
def authenticated_api_client_as_advisee(mock_advisee_user):
    api_client = APIClient()
    api_client.force_authenticate(mock_advisee_user)
    return api_client


@pytest.fixture
def mock_advisor_user():
    advisor = AdvisorFactory(email="advisor_0@email.com")
    return advisor


@pytest.fixture
def mock_relationship(mock_advisee_user, mock_advisor_user):
    relationship = AdvisorRelationshipFactory(
        advisee=mock_advisee_user, advisor=mock_advisor_user
    )
    return relationship


@pytest.fixture
def authenticated_api_client_as_advisor(mock_advisor_user):
    api_client = APIClient()
    api_client.force_authenticate(mock_advisor_user)
    return api_client


@pytest.fixture
def mock_currency():
    return CurrencyFactory(
        code="MCK",
        numeric_code="123",
        name="Mock Currency",
    )


@pytest.fixture
def mock_alternate_currency():
    return CurrencyFactory(
        code="MOC",
        numeric_code="567",
        name="Mock Alternate Currency",
    )
