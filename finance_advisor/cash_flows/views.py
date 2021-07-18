from rest_framework import mixins, permissions, viewsets

from finance_advisor.advisees.permissions import (
    IsAdviseeFilteredByUrlSelf,
    IsOwnedBySelf,
)
from finance_advisor.advisors.permissions import (
    IsAdviseeFilteredByUrlClient,
    IsOwnedByClient,
)
from finance_advisor.cash_flows.models import (
    Expense,
    ExpenseCategory,
    Income,
    IncomeCategory,
)
from finance_advisor.cash_flows.serializers import (
    ExpenseCategorySerializer,
    ExpenseSerializer,
    IncomeCategorySerializer,
    IncomeSerializer,
)


class AdviseeIncomeViewset(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    permission_classes = [
        (IsAdviseeFilteredByUrlClient & IsOwnedByClient)
        | (IsAdviseeFilteredByUrlSelf & IsOwnedBySelf)
    ]

    def get_queryset(self):
        """
        This view should return a list of all the incomes for
        a user as determined by the user id portion of the URL.
        """
        advisee_id = self.kwargs["advisee_id"]
        return Income.objects.filter(owner_id=advisee_id)

    def perform_create(self, serializer):
        serializer.save(owner_id=self.kwargs["advisee_id"])


class AdviseeExpenseViewset(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [
        (IsAdviseeFilteredByUrlClient & IsOwnedByClient)
        | (IsAdviseeFilteredByUrlSelf & IsOwnedBySelf)
    ]

    def get_queryset(self):
        """
        This view should return a list of all the expenses for
        a user as determined by the user id portion of the URL.
        """
        advisee_id = self.kwargs["advisee_id"]
        return Expense.objects.filter(owner_id=advisee_id)

    def perform_create(self, serializer):
        serializer.save(owner_id=self.kwargs["advisee_id"])


class CoreIncomeCategoryListViewset(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = IncomeCategory.objects.all()
    serializer_class = IncomeCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class CoreExpenseCategoryListViewset(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
