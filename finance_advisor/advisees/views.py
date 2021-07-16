from rest_framework import mixins, permissions, viewsets

from finance_advisor.advisees.models import Advisee
from finance_advisor.advisees.serializers import (
    AdviseeCreateSerializer,
    AdviseeSerializer,
)
from finance_advisor.advisors.permissions import IsClient
from finance_advisor.core.permissions import IsSafeRequest, IsSelf


class AdviseeRetrieveUpdateDestroyViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Advisee.objects.all()
    serializer_class = AdviseeSerializer
    permission_classes = [IsSelf | (IsSafeRequest & IsClient)]


class AdviseeCreateViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = AdviseeCreateSerializer
    permission_classes = [permissions.AllowAny]
