from rest_framework import serializers

from finance_advisor.advisors.models import Advisor


class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "gender",
            "date_of_birth",
            "profile_photo",
            "phone",
        ]
