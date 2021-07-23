from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from finance_advisor.core.models import Currency
from finance_advisor.core.utils.get_user_type import get_user_type


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = [
            "id",
            "name",
            "code",
            "numeric_code",
        ]


class TokenObtainPairWithUserInfoSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["user_type"] = get_user_type(user)

        return token

    def validate(self, attrs):
        attrs[self.username_field] = attrs[self.username_field].lower()

        data = super().validate(attrs)
        return data
