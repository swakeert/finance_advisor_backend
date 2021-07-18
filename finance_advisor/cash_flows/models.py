from django.db import models

from finance_advisor.advisees.models import Advisee
from finance_advisor.core.models import Currency


class IncomeCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Income Categories"

    def __str__(self) -> str:
        return self.name


class IncomeType(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(
        IncomeCategory,
        on_delete=models.PROTECT,
        related_name="income_types",
    )

    class Meta:
        ordering = (
            "category",
            "name",
        )

    def __str__(self) -> str:
        return f"{self.category}: {self.name}"


class Income(models.Model):
    owner = models.ForeignKey(Advisee, on_delete=models.CASCADE)
    annual_value = models.PositiveBigIntegerField(
        help_text="Post tax amount earned, per annum.",
    )
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    income_type = models.ForeignKey(
        IncomeType,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    notes = models.TextField(
        blank=True,
        help_text="Any additional information or comments.",
    )

    class Meta:
        ordering = (
            "owner",
            "income_type",
        )

    def __str__(self) -> str:
        return f"{self.owner} - {self.income_type}"


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Expense Categories"

    def __str__(self) -> str:
        return self.name


class ExpenseType(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.PROTECT,
        related_name="expense_types",
    )

    class Meta:
        ordering = (
            "category",
            "name",
        )

    def __str__(self) -> str:
        return f"{self.category}: {self.name}"


class Expense(models.Model):
    owner = models.ForeignKey(Advisee, on_delete=models.CASCADE)
    monthly_value = models.PositiveBigIntegerField(
        help_text="Expense per month on a rough average.",
    )
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    expense_type = models.ForeignKey(
        ExpenseType,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    notes = models.TextField(
        help_text="Any additional information or comments.",
    )

    class Meta:
        ordering = (
            "owner",
            "expense_type",
        )

    def __str__(self) -> str:
        return f"{self.owner} - {self.expense_type}"
