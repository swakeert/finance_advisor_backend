from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from finance_advisor.advisee.models import Advisee
from finance_advisor.core.models import CustomUser


class Advisor(CustomUser):
    clients = models.ManyToManyField(Advisee, through="AdvisorRelationship")


class RelationshipStatusChoices(models.TextChoices):
    INITIATED = "I", "Initiated"  # Started to talk, scheduled an appoint, etc.
    ESTABLISHED = "E", "Established"  # Current Financial advisor.
    TERMINATED = "T", "Terminated"  # Was established at some point, but not any more.
    OTHER = "O", "Others"  # Was initiated but not established or something else.


class AdvisorRelationship(models.Model):
    advisee = models.ForeignKey(Advisee, on_delete=models.CASCADE)
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE)
    relationship_status = models.CharField(
        max_length=1,
        choices=RelationshipStatusChoices.choices,
        blank=False,
    )

    def __str__(self) -> str:
        return f"{self.advisor} advisor to {self.advisee}"


class AdvisorRelationshipBilling(models.Model):
    relationship = models.ForeignKey(AdvisorRelationship, on_delete=models.CASCADE)
    billing_period_start = models.DateField()
    billing_period_end = models.DateField()
    billing_amount = models.IntegerField(
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.relationship} ({self.billing_period_start} to {self.billing_period_end})"


@receiver(pre_save, sender=Advisor)
def use_email_as_username(sender, instance, *args, **kwargs):
    instance.username = instance.email.lower()
