import pytest

from finance_advisor.advisors.tests.factory import AdvisorFactory


@pytest.fixture
def mock_alternate_advisor_user():
    advisor = AdvisorFactory(email="advisor_1@email.com")
    advisor.set_password("test_password")
    return advisor
