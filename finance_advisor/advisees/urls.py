from rest_framework import routers

from finance_advisor.advisees.views import (
    AdviseeCreateViewSet,
    AdviseeRetrieveUpdateDestroyViewSet,
)

advisee_router = routers.DefaultRouter()
advisee_router.register(
    "", AdviseeRetrieveUpdateDestroyViewSet, "advisee-retrieve-update-destroy"
)
advisee_router.register("", AdviseeCreateViewSet, "advisee-create")
