import factory

from finance_advisor.advisee.models import Advisee


class AdviseeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Advisee
        django_get_or_create = ("email",)
