import factory

from finance_advisor.advisees.tests.factory import AdviseeFactory
from finance_advisor.core.tests.factory import CurrencyFactory
from finance_advisor.goals.models import Goal


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    owner = factory.SubFactory(AdviseeFactory)
    currency = factory.SubFactory(CurrencyFactory)
