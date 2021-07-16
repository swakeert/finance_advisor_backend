from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from finance_advisor.advisee.models import Advisee

User = get_user_model()


class AdviseeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisee
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "gender",
            "date_of_birth",
            "profile_photo",
            "phone",
        )


class AdviseeCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Advisee
        fields = (
            "id",
            "email",
            "password",
            "password2",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        advisee = Advisee.objects.create(
            email=validated_data["email"],
        )

        advisee.set_password(validated_data["password"])
        advisee.save()

        return advisee
