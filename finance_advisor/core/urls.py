from rest_framework import routers

from finance_advisor.cash_flows.views import (
    CoreExpenseCategoryListViewset,
    CoreIncomeCategoryListViewset,
)
from finance_advisor.core.views import CurrencyReadOnlyViewSet

core_router = routers.DefaultRouter()
core_router.register("currencies", CurrencyReadOnlyViewSet)
core_router.register("incomes", CoreIncomeCategoryListViewset, "core-incomes")
core_router.register("expenses", CoreExpenseCategoryListViewset, "core-expenses")
