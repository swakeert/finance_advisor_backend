from rest_framework import mixins, permissions, viewsets

from finance_advisor.advisee.models import Advisee
from finance_advisor.advisee.permissions import AdviseePermission
from finance_advisor.advisee.serializers import (
    AdviseeCreateSerializer,
    AdviseeSerializer,
)


class AdviseeRetrieveUpdateDestroyViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Advisee.objects.all()
    serializer_class = AdviseeSerializer
    permission_classes = [permissions.IsAuthenticated & AdviseePermission]


class AdviseeCreateViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = AdviseeCreateSerializer
    permission_classes = [permissions.AllowAny]
