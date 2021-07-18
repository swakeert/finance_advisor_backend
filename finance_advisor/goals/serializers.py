from rest_framework import serializers

from finance_advisor.goals.models import Goal


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = (
            "id",
            "name",
            "value",
            "currency",
            "target_date",
        )
