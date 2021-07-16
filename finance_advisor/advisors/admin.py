from django.contrib import admin

from finance_advisor.advisors.models import (
    Advisor,
    AdvisorRelationship,
    AdvisorRelationshipBilling,
)


@admin.register(Advisor)
class AdvisorAdmin(admin.ModelAdmin):
    pass


@admin.register(AdvisorRelationship)
class AdvisorRelationshipAdmin(admin.ModelAdmin):
    pass


@admin.register(AdvisorRelationshipBilling)
class AdvisorRelationshipBillingAdmin(admin.ModelAdmin):
    pass
