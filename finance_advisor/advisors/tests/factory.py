import factory

from finance_advisor.advisees.tests.factory import AdviseeFactory
from finance_advisor.advisors.models import (
    Advisor,
    AdvisorRelationship,
    AdvisorRelationshipBilling,
)


class AdvisorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Advisor
        django_get_or_create = ("email",)


class AdvisorRelationshipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AdvisorRelationship
        django_get_or_create = ("advisee", "advisor")

    advisee = factory.SubFactory(AdviseeFactory)
    advisor = factory.SubFactory(AdvisorFactory)


class AdvisorRelationshipBillingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AdvisorRelationshipBilling
        django_get_or_create = ("relationship",)

    relationship = factory.SubFactory(AdvisorRelationshipFactory)
