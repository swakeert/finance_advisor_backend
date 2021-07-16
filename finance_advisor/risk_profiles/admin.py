from django.contrib import admin

from finance_advisor.risk_profiles.models import (
    RiskAssessmentquestionnaire,
    RiskProfile,
)


@admin.register(RiskProfile)
class RiskProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(RiskAssessmentquestionnaire)
class RiskAssessmentquestionnaireAdmin(admin.ModelAdmin):
    pass
