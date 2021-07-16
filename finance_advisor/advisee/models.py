from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from finance_advisor.core.models import CustomUser


class Advisee(CustomUser):
    pass


@receiver(pre_save, sender=Advisee)
def use_email_as_username(sender, instance, *args, **kwargs):
    instance.username = instance.email.lower()
