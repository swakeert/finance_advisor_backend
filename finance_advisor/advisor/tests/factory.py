import factory

from finance_advisor.advisee.tests.factory import AdviseeFactory
from finance_advisor.advisor.models import (
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
        django_get_or_create = ("email",)

    advisee = factory.SubFactory(AdviseeFactory)
    advisor = factory.SubFactory(AdvisorFactory)


class AdvisorRelationshipBillingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AdvisorRelationshipBilling
        django_get_or_create = ("email",)

    relationship = factory.SubFactory(AdvisorRelationshipFactory)
