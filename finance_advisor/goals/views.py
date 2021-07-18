from rest_framework import mixins, permissions, viewsets

from finance_advisor.advisees.permissions import (
    IsAdviseeFilteredByUrlSelf,
    IsOwnedBySelf,
)
from finance_advisor.advisors.permissions import (
    IsAdviseeFilteredByUrlClient,
    IsOwnedByClient,
)
from finance_advisor.goals.models import Goal
from finance_advisor.goals.serializers import GoalSerializer


class GoalViewset(
    viewsets.ModelViewSet,
):
    serializer_class = GoalSerializer
    permission_classes = [
        (IsAdviseeFilteredByUrlClient & IsOwnedByClient)
        | (IsAdviseeFilteredByUrlSelf & IsOwnedBySelf)
    ]

    def get_queryset(self):
        """
        This view should return a list of all the goals for
        a user as determined by the user id portion of the URL.
        """
        advisee_id = self.kwargs["advisee_id"]
        return Goal.objects.filter(owner_id=advisee_id)

    def perform_create(self, serializer):
        serializer.save(owner_id=self.kwargs["advisee_id"])
