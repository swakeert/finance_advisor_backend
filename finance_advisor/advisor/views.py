from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets

from finance_advisor.advisor.models import Advisor
from finance_advisor.advisor.serializers import AdvisorSerializer
from finance_advisor.core.permissions import IsSafeRequest, IsSelf


class AdvisorReadOnlyViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filter_fields = [
        "first_name",
        "last_name",
        "email",
        "gender",
        "date_of_birth",
    ]

    filterset_fields = {
        "date_of_birth": ["gte", "lte"],
    }


class AdvisorRetrieveUpdateDestroyViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer
    permission_classes = [IsSelf | IsSafeRequest]
