from rest_framework import serializers

from finance_advisor.core.models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = [
            "id",
            "name",
            "code",
            "numeric_code",
        ]
