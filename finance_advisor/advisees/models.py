from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from finance_advisor.core.models import CustomUser


class Family(models.Model):
    pass

    class Meta:
        verbose_name = "Family"
        verbose_name_plural = "Families"

    def __str__(self) -> str:
        return f"{self.members.first()}'s family"


class Advisee(CustomUser):
    family = models.ForeignKey(
        Family,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="members",
    )

    # TODO: Preference for online/ offline. Location. Preference for city, area, country.
    # Full address for legal purposes? Document store?

    class Meta:
        verbose_name = "Advisee"
        verbose_name_plural = "Advisees"
        ordering = ("first_name", "last_name", "username")


@receiver(pre_save, sender=Advisee)
def use_email_as_username(sender, instance, *args, **kwargs):
    if instance.email:
        instance.username = instance.email.lower()
