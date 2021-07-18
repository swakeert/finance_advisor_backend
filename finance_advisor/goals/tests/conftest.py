import pytest

from finance_advisor.goals.tests.factory import GoalFactory


@pytest.fixture
def mock_goal(mock_advisee_user, mock_currency):
    return GoalFactory(
        owner=mock_advisee_user,
        currency=mock_currency,
        name="Goal 0",
        value=0,
        target_date="2021-01-01",
    )


@pytest.fixture
def mock_alternate_users_goal(mock_alternate_advisee_user, mock_currency):
    return GoalFactory(
        owner=mock_alternate_advisee_user,
        currency=mock_currency,
        name="Goal 1",
        value=1,
        target_date="2021-02-02",
    )
