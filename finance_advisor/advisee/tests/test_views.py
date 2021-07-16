import pytest
from django.contrib.auth import authenticate
from rest_framework.test import APIClient

from finance_advisor.advisee.tests.factory import AdviseeFactory
from finance_advisor.advisor.tests.factory import (
    AdvisorFactory,
    AdvisorRelationshipFactory,
)


@pytest.fixture
def advisee_user():
    advisee = AdviseeFactory(email="fake_advisee@email.com")
    advisee.set_password("test_password")
    return advisee


@pytest.fixture
def advisor_user():
    advisor = AdvisorFactory(email="fake_advisor@email.com")
    advisor.set_password("test_password")
    return advisor


@pytest.fixture
def relationship(advisee_user, advisor_user):
    relationship = AdvisorRelationshipFactory(
        advisee=advisee_user, advisor=advisor_user
    )
    return relationship


@pytest.fixture
def authenticated_api_client_as_advisee(advisee_user):
    client = APIClient()
    client.force_authenticate(advisee_user)
    return client


@pytest.fixture
def authenticated_api_client_as_advisor(advisor_user):
    client = APIClient()
    client.force_authenticate(advisor_user)
    return client


def test_create_supports_only_post():
    client = APIClient()
    response = client.get("/api/v1/advisee/")
    assert response.status_code == 405
    response = client.put("/api/v1/advisee/")
    assert response.status_code == 405


@pytest.mark.django_db
def test_create_validates_password():
    client = APIClient()
    response = client.post(
        "/api/v1/advisee/",
        {
            "email": "fake_advisee@email.com",
            "password": "test_password",
            "password2": "different_password",
        },
    )
    assert response.status_code == 400

    response = client.post(
        "/api/v1/advisee/",
        {
            "email": "fake_advisee@email.com",
            "password": "weak",
            "password2": "weak",
        },
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_validates_email(advisee_user):
    client = APIClient()
    response = client.post(
        "/api/v1/advisee/",
        {
            "email": "fake_advisee@email.com",
            "password": "test_password",
            "password2": "test_password",
        },
    )
    assert response.status_code == 400

    response = client.post(
        "/api/v1/advisee/",
        {
            "email": "not email",
            "password": "test_password",
            "password2": "test_password",
        },
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_works_and_stores_lowercase_email_as_username():
    client = APIClient()
    response = client.post(
        "/api/v1/advisee/",
        {
            "email": "FaKe_advisee@Email.com",
            "password": "test_password",
            "password2": "test_password",
        },
    )
    assert response.status_code == 201
    assert response.data["email"] == "FaKe_advisee@Email.com"

    user = authenticate(  # nosec
        username="fake_advisee@email.com",
        password="test_password",
    )
    assert user is not None
    assert user.username == "fake_advisee@email.com"


@pytest.mark.django_db
def test_unauthenticated_request_forbidden(advisee_user):
    client = APIClient()
    response = client.get("/api/v1/advisee/1/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_does_return_self(advisee_user, authenticated_api_client_as_advisee):
    response = authenticated_api_client_as_advisee.get(
        f"/api/v1/advisee/{advisee_user.id}/"
    )
    assert response.status_code == 200
    assert response.data == {
        "id": 1,
        "email": "fake_advisee@email.com",
        "first_name": "",
        "last_name": "",
        "gender": "",
        "date_of_birth": None,
        "profile_photo": None,
        "phone": "",
    }


@pytest.mark.django_db
def test_can_partial_update_self(advisee_user, authenticated_api_client_as_advisee):
    response = authenticated_api_client_as_advisee.patch(
        f"/api/v1/advisee/{advisee_user.id}/",
        {
            "first_name": "John",
            "last_name": "Doe",
        },
    )
    assert response.status_code == 200
    assert response.data == {
        "id": 1,
        "email": "fake_advisee@email.com",
        "first_name": "John",
        "last_name": "Doe",
        "gender": "",
        "date_of_birth": None,
        "profile_photo": None,
        "phone": "",
    }


@pytest.mark.django_db
def test_can_full_update_self(advisee_user, authenticated_api_client_as_advisee):
    response = authenticated_api_client_as_advisee.patch(
        f"/api/v1/advisee/{advisee_user.id}/",
        {
            "email": "fake2@email.com",
            "first_name": "John",
            "last_name": "Doe",
            "gender": "N",
            "date_of_birth": "2018-01-01",
            "phone": "1234567890",
        },
    )
    assert response.status_code == 200
    assert response.data == {
        "id": 1,
        "email": "fake2@email.com",
        "first_name": "John",
        "last_name": "Doe",
        "gender": "N",
        "date_of_birth": "2018-01-01",
        "profile_photo": None,
        "phone": "1234567890",
    }


@pytest.mark.django_db
def test_does_not_return_other_users(authenticated_api_client_as_advisee):
    advisee_2 = AdviseeFactory(email="fake2@email.com")
    response = authenticated_api_client_as_advisee.get(
        f"/api/v1/advisee/{advisee_2.id}/"
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_advisor_can_access_client(
    advisee_user,
    advisor_user,
    relationship,
    authenticated_api_client_as_advisor,
):
    response = authenticated_api_client_as_advisor.get(
        f"/api/v1/advisee/{advisee_user.id}/"
    )
    assert response.status_code == 200
    assert response.data == {
        "id": 1,
        "email": "fake_advisee@email.com",
        "first_name": "",
        "last_name": "",
        "gender": "",
        "date_of_birth": None,
        "profile_photo": None,
        "phone": "",
    }


@pytest.mark.django_db
def test_advisor_cannot_access_non_clients(
    advisor_user,
    relationship,
    authenticated_api_client_as_advisor,
):
    advisee_2 = AdviseeFactory(email="fake_advisee_2@email.com")

    response = authenticated_api_client_as_advisor.get(
        f"/api/v1/advisee/{advisee_2.id}/"
    )
    assert response.status_code == 403
