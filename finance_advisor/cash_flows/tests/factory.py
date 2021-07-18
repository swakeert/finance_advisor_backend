import factory

from finance_advisor.advisees.tests.factory import AdviseeFactory
from finance_advisor.cash_flows.models import (
    Expense,
    ExpenseCategory,
    ExpenseType,
    Income,
    IncomeCategory,
    IncomeType,
)
from finance_advisor.core.tests.factory import CurrencyFactory


class IncomeCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IncomeCategory


class IncomeTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IncomeType

    category = factory.SubFactory(IncomeCategory)


class IncomeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Income

    owner = factory.SubFactory(AdviseeFactory)
    currency = factory.SubFactory(CurrencyFactory)
    income_type = factory.SubFactory(IncomeTypeFactory)


class ExpenseCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExpenseCategory


class ExpenseTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExpenseType

    category = factory.SubFactory(ExpenseCategory)


class ExpenseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Expense

    owner = factory.SubFactory(AdviseeFactory)
    currency = factory.SubFactory(CurrencyFactory)
    expense_type = factory.SubFactory(ExpenseTypeFactory)
