from django.urls import include, path
from rest_framework import routers

from finance_advisor.goals.views import GoalViewset

goal_router = routers.DefaultRouter()
goal_router.register("", GoalViewset, "goals")
