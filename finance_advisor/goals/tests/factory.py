from datetime import date, timedelta

import factory

from finance_advisor.advisees.tests.factory import AdviseeFactory
from finance_advisor.core.tests.factory import CurrencyFactory
from finance_advisor.goals.models import Goal


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    owner = factory.SubFactory(AdviseeFactory)
    name = factory.Sequence(lambda n: f"Goal {n}")
    value = factory.Sequence(lambda n: n * 100)
    target_date = factory.Sequence(lambda n: date(2021, 1, 1) + timedelta(days=n))
    currency = factory.SubFactory(CurrencyFactory)
