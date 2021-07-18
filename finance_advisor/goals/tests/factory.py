from datetime import date, timedelta

import factory
import pytest

from finance_advisor.advisees.tests.factory import (
    AdviseeFactory,
    mock_advisee_user,
    mock_alternate_advisee_user,
)
from finance_advisor.core.tests.factory import CurrencyFactory, mock_currency
from finance_advisor.goals.models import Goal


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    owner = factory.SubFactory(AdviseeFactory)
    name = factory.Sequence(lambda n: f"Goal {n}")
    value = factory.Sequence(lambda n: n * 100)
    target_date = factory.Sequence(lambda n: date(2021, 1, 1) + timedelta(days=n))
    currency = factory.SubFactory(CurrencyFactory)


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
