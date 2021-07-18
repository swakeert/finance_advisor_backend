import pytest
from django.contrib.auth import authenticate
from rest_framework.test import APIClient

from finance_advisor.advisees.models import Advisee
from finance_advisor.advisees.tests.factory import (
    AdviseeFactory,
    authenticated_api_client_as_advisee,
    mock_advisee_user,
    mock_alternate_advisee_user,
)
from finance_advisor.advisors.tests.factory import (
    authenticated_api_client_as_advisor,
    mock_advisor_user,
    mock_relationship,
)


def test_create_supports_only_post():
    api_client = APIClient()
    response = api_client.get("/api/v1/advisees/")
    assert response.status_code == 405
    response = api_client.put("/api/v1/advisees/")
    assert response.status_code == 405


@pytest.mark.django_db
def test_create_validates_password():
    api_client = APIClient()
    response = api_client.post(
        "/api/v1/advisees/",
        {
            "email": "advisee_0@email.com",
            "password": "test_password",
            "password2": "different_password",
        },
    )
    assert response.status_code == 400

    response = api_client.post(
        "/api/v1/advisees/",
        {
            "email": "advisee_0@email.com",
            "password": "weak",
            "password2": "weak",
        },
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_validates_email(mock_advisee_user):
    api_client = APIClient()
    response = api_client.post(
        "/api/v1/advisees/",
        {
            "email": "advisee_0@email.com",
            "password": "test_password",
            "password2": "test_password",
        },
    )
    assert response.status_code == 400

    response = api_client.post(
        "/api/v1/advisees/",
        {
            "email": "not email",
            "password": "test_password",
            "password2": "test_password",
        },
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_works_and_stores_lowercase_email_as_username():
    api_client = APIClient()
    response = api_client.post(
        "/api/v1/advisees/",
        {
            "email": "AdvIseE_0@Email.com",
            "password": "test_password",
            "password2": "test_password",
        },
    )
    assert response.status_code == 201
    assert response.data["email"] == "AdvIseE_0@Email.com"

    user = authenticate(  # nosec
        username="advisee_0@email.com",
        password="test_password",
    )
    assert user is not None
    assert user.username == "advisee_0@email.com"


@pytest.mark.django_db
def test_unauthenticated_request_forbidden(mock_advisee_user):
    api_client = APIClient()
    response = api_client.get("/api/v1/advisees/1/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_does_return_self(mock_advisee_user, authenticated_api_client_as_advisee):
    response = authenticated_api_client_as_advisee.get(
        f"/api/v1/advisees/{mock_advisee_user.id}/"
    )
    assert response.status_code == 200
    assert response.data == {
        "id": 1,
        "email": "advisee_0@email.com",
        "first_name": "",
        "last_name": "",
        "gender": "",
        "date_of_birth": None,
        "profile_photo": None,
        "phone": "",
    }


@pytest.mark.django_db
def test_can_partial_update_self(
    mock_advisee_user, authenticated_api_client_as_advisee
):
    response = authenticated_api_client_as_advisee.patch(
        f"/api/v1/advisees/{mock_advisee_user.id}/",
        {
            "first_name": "John",
            "last_name": "Doe",
        },
    )
    assert response.status_code == 200
    assert response.data == {
        "id": 1,
        "email": "advisee_0@email.com",
        "first_name": "John",
        "last_name": "Doe",
        "gender": "",
        "date_of_birth": None,
        "profile_photo": None,
        "phone": "",
    }


@pytest.mark.django_db
def test_can_full_update_self(mock_advisee_user, authenticated_api_client_as_advisee):
    response = authenticated_api_client_as_advisee.put(
        f"/api/v1/advisees/{mock_advisee_user.id}/",
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


@pytest.mark.skip
def test_can_update_profile_photo():
    pass


@pytest.mark.django_db
def test_can_delete_self(mock_advisee_user, authenticated_api_client_as_advisee):
    response = authenticated_api_client_as_advisee.delete(
        f"/api/v1/advisees/{mock_advisee_user.id}/",
    )
    assert response.status_code == 204

    assert Advisee.objects.filter(id=mock_advisee_user.id).count() == 0


@pytest.mark.django_db
def test_does_not_return_other_users(
    authenticated_api_client_as_advisee,
    mock_alternate_advisee_user,
):
    response = authenticated_api_client_as_advisee.get(
        f"/api/v1/advisees/{mock_alternate_advisee_user.id}/"
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_advisor_can_access_client(
    mock_advisee_user,
    mock_advisor_user,
    mock_relationship,
    authenticated_api_client_as_advisor,
):
    response = authenticated_api_client_as_advisor.get(
        f"/api/v1/advisees/{mock_advisee_user.id}/"
    )
    assert response.status_code == 200
    assert response.data == {
        "id": 1,
        "email": "advisee_0@email.com",
        "first_name": "",
        "last_name": "",
        "gender": "",
        "date_of_birth": None,
        "profile_photo": None,
        "phone": "",
    }


@pytest.mark.django_db
def test_advisor_cannot_access_non_clients(
    mock_advisor_user,
    mock_relationship,
    authenticated_api_client_as_advisor,
    mock_alternate_advisee_user,
):
    response = authenticated_api_client_as_advisor.get(
        f"/api/v1/advisees/{mock_alternate_advisee_user.id}/"
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_advisor_cannot_modify_clients(
    mock_advisor_user,
    mock_advisee_user,
    mock_relationship,
    authenticated_api_client_as_advisor,
):
    payload = [
        f"/api/v1/advisees/{mock_advisee_user.id}/",
        {
            "email": "fake2@email.com",
            "first_name": "John",
            "last_name": "Doe",
            "gender": "N",
            "date_of_birth": "2018-01-01",
            "phone": "1234567890",
        },
    ]

    response = authenticated_api_client_as_advisor.post(*payload)
    assert response.status_code == 405

    response = authenticated_api_client_as_advisor.put(*payload)
    assert response.status_code == 403

    response = authenticated_api_client_as_advisor.delete(
        f"/api/v1/advisees/{mock_advisee_user.id}/",
    )
    assert response.status_code == 403
