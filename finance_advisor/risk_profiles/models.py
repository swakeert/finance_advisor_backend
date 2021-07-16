from django.db import models

from finance_advisor.advisees.models import Advisee


class RiskProfileChoices(models.TextChoices):
    # TODO: Refine choices.
    LOW = "L", "Low"
    MEDIUM = "M", "Medium"
    HIGH = "H", "High"


class RiskAssessmentEducationChoices(models.TextChoices):
    # TODO: Refine choices.
    SCHOOL = "S", "Up to 12th"
    BACHELORS = "B", "Bachelor’s Degree"
    MASTERS = "M", "Master’s Degree"


class RiskProfile(models.Model):
    advisee = models.OneToOneField(Advisee, on_delete=models.CASCADE)
    assessment = models.CharField(
        max_length=1,
        choices=RiskProfileChoices.choices,
        blank=True,
    )
    assessment_last_updated = models.DateTimeField(
        blank=True,
        null=True,
    )


class RiskAssessmentquestionnaire(models.Model):
    # Education is example question. This questionnaire should contain questions about mentality.
    # TODO: Check if dynamic django forms might be a better replacement
    # https://pypi.org/project/dynamic-django-forms/
    advisee = models.ForeignKey(Advisee, on_delete=models.CASCADE)
    filled_date = models.DateTimeField(auto_now=True)
    education = models.CharField(
        max_length=1,
        choices=RiskAssessmentEducationChoices.choices,
    )
