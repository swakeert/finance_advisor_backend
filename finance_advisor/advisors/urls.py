from django.urls import include, path
from rest_framework import routers

from finance_advisor.advisors.views import (
    AdvisorReadOnlyViewSet,
    AdvisorRetrieveUpdateDestroyViewSet,
)

advisor_router = routers.DefaultRouter()
advisor_router.register("", AdvisorReadOnlyViewSet)
advisor_router.register("", AdvisorRetrieveUpdateDestroyViewSet)
