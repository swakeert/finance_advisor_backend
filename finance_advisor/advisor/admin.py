from django.contrib import admin

from finance_advisor.advisor.models import Advisor


@admin.register(Advisor)
class AdvisorAdmin(admin.ModelAdmin):
    pass
