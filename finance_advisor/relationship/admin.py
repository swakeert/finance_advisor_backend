from django.contrib import admin

from finance_advisor.relationship.models import (
    AdivsorRelationshipBilling,
    AdvisorRelationship,
)


@admin.register(AdvisorRelationship)
class AdvisorRelationshipAdmin(admin.ModelAdmin):
    pass


@admin.register(AdivsorRelationshipBilling)
class AdvisorRelationshipBillingAdmin(admin.ModelAdmin):
    pass
