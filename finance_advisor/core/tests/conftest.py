import pytest

from finance_advisor.core.tests.factory import CurrencyFactory


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
