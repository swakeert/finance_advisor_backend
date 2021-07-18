from rest_framework import serializers

from finance_advisor.cash_flows.models import (
    Expense,
    ExpenseCategory,
    ExpenseType,
    Income,
    IncomeCategory,
    IncomeType,
)


class IncomeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeType
        fields = (
            "id",
            "name",
        )


class IncomeCategorySerializer(serializers.ModelSerializer):
    income_types = IncomeTypeSerializer(many=True, read_only=True)

    class Meta:
        model = IncomeCategory
        fields = (
            "id",
            "name",
            "income_types",
        )


class IncomeSerializer(serializers.ModelSerializer):
    annual_value = serializers.IntegerField(min_value=0)

    class Meta:
        model = Income
        fields = (
            "id",
            "annual_value",
            "currency",
            "income_type",
            "notes",
        )


class ExpenseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseType
        fields = (
            "id",
            "name",
        )


class ExpenseCategorySerializer(serializers.ModelSerializer):
    expense_types = ExpenseTypeSerializer(many=True, read_only=True)

    class Meta:
        model = ExpenseCategory
        fields = (
            "id",
            "name",
            "expense_types",
        )


class ExpenseSerializer(serializers.ModelSerializer):
    monthly_value = serializers.IntegerField(min_value=0)

    class Meta:
        model = Expense
        fields = (
            "id",
            "monthly_value",
            "currency",
            "expense_type",
            "notes",
        )
