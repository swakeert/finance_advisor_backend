from django.contrib import admin

from finance_advisor.goals.models import Goal


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    pass
