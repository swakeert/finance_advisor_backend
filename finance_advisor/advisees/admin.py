from django.contrib import admin

from finance_advisor.advisees.models import Advisee, Family


@admin.register(Advisee)
class AdviseeAdmin(admin.ModelAdmin):
    pass


class AdviseeInlineAdmin(admin.TabularInline):
    model = Advisee
    fields = (
        "email",
        "first_name",
        "last_name",
    )
    readonly_fields = (
        "email",
        "first_name",
        "last_name",
    )
    extra = 0


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    inlines = (AdviseeInlineAdmin,)
