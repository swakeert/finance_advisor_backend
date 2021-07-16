from django.contrib import admin

from finance_advisor.advisees.models import Advisee


@admin.register(Advisee)
class AdviseeAdmin(admin.ModelAdmin):
    pass
