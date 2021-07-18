from rest_framework import routers

from finance_advisor.core.views import CurrencyReadOnlyViewSet

core_router = routers.DefaultRouter()
core_router.register("currencies", CurrencyReadOnlyViewSet)
