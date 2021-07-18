import pytest

from finance_advisor.cash_flows.tests.factory import (
    ExpenseCategoryFactory,
    ExpenseFactory,
    ExpenseTypeFactory,
    IncomeCategoryFactory,
    IncomeFactory,
    IncomeTypeFactory,
)


@pytest.fixture
def mock_income_category():
    return IncomeCategoryFactory(name="Income Category 1")


@pytest.fixture
def mock_income_type(mock_income_category):
    return IncomeTypeFactory(
        name="Income Type 1",
        category=mock_income_category,
    )


@pytest.fixture
def mock_alternate_income_category():
    return IncomeCategoryFactory(name="Income Category 2")


@pytest.fixture
def mock_alternate_income_type(mock_alternate_income_category):
    return IncomeTypeFactory(
        name="Income Type 2",
        category=mock_alternate_income_category,
    )


@pytest.fixture
def mock_income(mock_advisee_user, mock_income_type, mock_currency):
    return IncomeFactory(
        owner=mock_advisee_user,
        annual_value=1000,
        currency=mock_currency,
        income_type=mock_income_type,
        notes="My first salary",
    )


@pytest.fixture
def mock_alternate_users_income(
    mock_alternate_advisee_user, mock_alternate_income_type, mock_alternate_currency
):
    return IncomeFactory(
        owner=mock_alternate_advisee_user,
        annual_value=2000,
        currency=mock_alternate_currency,
        income_type=mock_alternate_income_type,
        notes="Alternate's first salary",
    )


@pytest.fixture
def mock_expense_category():
    return ExpenseCategoryFactory(name="Expense Category 1")


@pytest.fixture
def mock_expense_type(mock_expense_category):
    return ExpenseTypeFactory(
        name="Expense Type 1",
        category=mock_expense_category,
    )


@pytest.fixture
def mock_alternate_expense_category():
    return ExpenseCategoryFactory(name="Expense Category 2")


@pytest.fixture
def mock_alternate_expense_type(mock_alternate_expense_category):
    return ExpenseTypeFactory(
        name="Expense Type 2",
        category=mock_alternate_expense_category,
    )


@pytest.fixture
def mock_expense(mock_advisee_user, mock_expense_type, mock_currency):
    return ExpenseFactory(
        owner=mock_advisee_user,
        monthly_value=1000,
        currency=mock_currency,
        expense_type=mock_expense_type,
        notes="My first expense",
    )


@pytest.fixture
def mock_alternate_users_expense(
    mock_alternate_advisee_user, mock_alternate_expense_type, mock_alternate_currency
):
    return ExpenseFactory(
        owner=mock_alternate_advisee_user,
        monthly_value=2000,
        currency=mock_alternate_currency,
        expense_type=mock_alternate_expense_type,
        notes="Alternate's first expense",
    )
