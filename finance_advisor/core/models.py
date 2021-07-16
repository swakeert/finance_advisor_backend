from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

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
        blank=True,
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )
    profile_photo = models.ImageField(
        upload_to="uploads/profile_photos/",
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.username

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
        ordering = ("first_name", "last_name", "username")


@receiver(pre_save, sender=CustomUser)
def use_email_as_username(sender, instance, *args, **kwargs):
    if instance.email:
        instance.username = instance.email.lower()


class Currency(models.Model):
    """
    Model to hold currency information. Imported from pycountries via a migration.
    See ISO 4217 for information on the currency itself. Or checkout pycountry's github.
    """

    code = models.CharField(
        max_length=3,
        # TODO: Implement min_length = 3 validation.
    )
    numeric_code = models.CharField(
        max_length=3,
        # TODO: Implement min_length = 3 validation.
    )
    name = models.CharField(
        max_length=100,
        help_text="Human Readable name for currency.",
    )

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name_plural = "Currencies"
        ordering = ("code",)
