import factory
import pytest

from finance_advisor.core.models import Currency


class CurrencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Currency


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
