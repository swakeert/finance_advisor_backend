from django.db import models

from finance_advisor.advisees.models import Advisee
from finance_advisor.core.models import Currency


class Goal(models.Model):
    owner = models.ForeignKey(Advisee, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    value = models.PositiveBigIntegerField()
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    target_date = models.DateField(
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.owner} - {self.name}"
