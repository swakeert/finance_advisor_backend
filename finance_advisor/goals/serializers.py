from rest_framework import serializers

from finance_advisor.goals.models import Goal


class GoalSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(min_value=0)

    class Meta:
        model = Goal
        fields = (
            "id",
            "name",
            "value",
            "currency",
            "target_date",
        )
