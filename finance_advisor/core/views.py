from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from finance_advisor.core.models import Currency
from finance_advisor.core.serializers import (
    CurrencySerializer,
    TokenObtainPairWithUserInfoSerializer,
)


class CurrencyReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "name",
        "code",
        "numeric_code",
    ]


class TokenObtainPairWithUserInfoView(TokenObtainPairView):
    serializer_class = TokenObtainPairWithUserInfoSerializer
