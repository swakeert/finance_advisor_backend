import pytest
from rest_framework.test import APIClient

from finance_advisor.advisors.tests.factory import (
    AdvisorFactory,
    AdvisorRelationshipFactory,
)


@pytest.fixture
def mock_alternate_advisor_user():
    advisor = AdvisorFactory(email="advisor_1@email.com")
    advisor.set_password("test_password")
    return advisor


@pytest.fixture
def mock_advisor_user():
    advisor = AdvisorFactory(email="advisor_0@email.com")
    advisor.set_password("test_password")
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
