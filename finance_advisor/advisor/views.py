from rest_framework import permissions, viewsets

from finance_advisor.advisor.models import Advisor
from finance_advisor.advisor.serializers import AdvisorSerializer


class AdvisorViewSet(viewsets.ModelViewSet):
    # TODO: Limit permissions. Remove List view.
    queryset = Advisor.objects.all()
    serializer_class = AdvisorSerializer
    permission_classes = [permissions.IsAuthenticated]
