from django.contrib import admin

from finance_advisor.core.models import Currency, CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    readonly_fields = ("code", "name", "numeric_code")
