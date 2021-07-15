from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class GenderChoices(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female"
    OTHER = "O", "Other"
    NOT_PROVIDED = "N", "Prefer not to say"


class CustomUser(User):
    phone = models.CharField(
        max_length=10,
        blank=True,
    )  # TODO: Add min length validator. Optionally, use 3rd party package for international extensibility and OTP implementation.
    gender = models.CharField(
        max_length=1,
        choices=GenderChoices.choices,
        blank=False,
    )
    date_of_birth = models.DateField(
        blank=False,
    )
    profile_photo = models.ImageField(
        upload_to="uploads/profile_photos/",
        blank=True,
    )

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.username
