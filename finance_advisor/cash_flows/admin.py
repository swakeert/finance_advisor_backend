from django.contrib import admin

from finance_advisor.cash_flows.models import (
    Expense,
    ExpenseCategory,
    ExpenseType,
    Income,
    IncomeCategory,
    IncomeType,
)


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    pass


class IncomeTypeInlineAdmin(admin.TabularInline):
    model = IncomeType


@admin.register(IncomeCategory)
class IncomeCategoryAdmin(admin.ModelAdmin):
    inlines = (IncomeTypeInlineAdmin,)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    pass


class ExpenseTypeInlineAdmin(admin.TabularInline):
    model = ExpenseType


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    inlines = (ExpenseTypeInlineAdmin,)
