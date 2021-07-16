from django.urls import include, path
from rest_framework import routers

from finance_advisor.advisor.views import AdvisorViewSet

advisor_router = routers.DefaultRouter()
advisor_router.register("", AdvisorViewSet)
