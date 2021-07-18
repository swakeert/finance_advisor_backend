from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from finance_advisor.advisees.models import Advisee

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


def case_insensitive_email_validation(data):
    """
    Check for case insensitive validation on email field
    """
    duplicate_exists = User.objects.filter(email__iexact=data).exists()
    if duplicate_exists:
        raise serializers.ValidationError("Email already in use.")
    return data


class AdviseeCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            case_insensitive_email_validation,
        ],
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
