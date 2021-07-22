import factory

from finance_advisor.advisees.models import Advisee


class AdviseeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Advisee
        django_get_or_create = ("email",)

    password = factory.PostGenerationMethodCall("set_password", "test_password")
