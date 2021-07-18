import pytest
from django.contrib.auth import authenticate
from rest_framework.test import APIClient

from finance_advisor.advisees.tests.factory import (
    AdviseeFactory,
    authenticated_api_client_as_advisee,
    mock_advisee_user,
)
from finance_advisor.advisors.models import Advisor
from finance_advisor.advisors.tests.factory import (
    AdvisorFactory,
    authenticated_api_client_as_advisor,
    mock_advisor_user,
    mock_alternate_advisor_user,
    mock_relationship,
)


def test_unauthenticated_cannot_list():
    api_client = APIClient()
    response = api_client.get("/api/v1/advisors/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_authenticated_can_list(
    authenticated_api_client_as_advisee,
    authenticated_api_client_as_advisor,
):
    response = authenticated_api_client_as_advisee.get("/api/v1/advisors/")
    assert response.status_code == 200

    response = authenticated_api_client_as_advisor.get("/api/v1/advisors/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_supports_only_list(
    authenticated_api_client_as_advisee,
    authenticated_api_client_as_advisor,
):
    response = authenticated_api_client_as_advisee.post("/api/v1/advisors/")
    assert response.status_code == 405
    response = authenticated_api_client_as_advisee.put("/api/v1/advisors/")
    assert response.status_code == 405
    response = authenticated_api_client_as_advisee.delete("/api/v1/advisors/")
    assert response.status_code == 405

    response = authenticated_api_client_as_advisor.post("/api/v1/advisors/")
    assert response.status_code == 405
    response = authenticated_api_client_as_advisor.put("/api/v1/advisors/")
    assert response.status_code == 405
    response = authenticated_api_client_as_advisor.delete("/api/v1/advisors/")
    assert response.status_code == 405


@pytest.mark.django_db
def test_advisee_can_readonly_any_advisor(
    authenticated_api_client_as_advisee,
    mock_advisor_user,
):
    response = authenticated_api_client_as_advisee.get(
        f"/api/v1/advisors/{mock_advisor_user.id}/"
    )
    assert response.status_code == 200
    assert response.data == {
        "id": 2,
        "email": "advisor_0@email.com",
        "first_name": "",
        "last_name": "",
        "gender": "",
        "date_of_birth": None,
        "profile_photo": None,
        "phone": "",
    }

    response = authenticated_api_client_as_advisee.put(
        f"/api/v1/advisors/{mock_advisor_user.id}/"
    )
    assert response.status_code == 403
    response = authenticated_api_client_as_advisee.delete(
        f"/api/v1/advisors/{mock_advisor_user.id}/"
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_advisor_can_readonly_any_advisor(
    authenticated_api_client_as_advisor,
    mock_alternate_advisor_user,
):
    response = authenticated_api_client_as_advisor.get(
        f"/api/v1/advisors/{mock_alternate_advisor_user.id}/"
    )
    assert response.status_code == 200
    assert response.data == {
        "id": 2,
        "email": "advisor_1@email.com",
        "first_name": "",
        "last_name": "",
        "gender": "",
        "date_of_birth": None,
        "profile_photo": None,
        "phone": "",
    }

    response = authenticated_api_client_as_advisor.put(
        f"/api/v1/advisors/{mock_alternate_advisor_user.id}/"
    )
    assert response.status_code == 403
    response = authenticated_api_client_as_advisor.delete(
        f"/api/v1/advisors/{mock_alternate_advisor_user.id}/"
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_advisor_can_read_self(
    authenticated_api_client_as_advisor,
    mock_advisor_user,
):
    response = authenticated_api_client_as_advisor.get(
        f"/api/v1/advisors/{mock_advisor_user.id}/"
    )
    assert response.status_code == 200
    assert response.data == {
        "id": 1,
        "email": "advisor_0@email.com",
        "first_name": "",
        "last_name": "",
        "gender": "",
        "date_of_birth": None,
        "profile_photo": None,
        "phone": "",
    }


@pytest.mark.django_db
def test_advisor_can_update_self(
    authenticated_api_client_as_advisor,
    mock_advisor_user,
):
    response = authenticated_api_client_as_advisor.put(
        f"/api/v1/advisors/{mock_advisor_user.id}/",
        {
            "email": "AdvIsoR_0@new-email.com",
            "first_name": "Test",
            "last_name": "Name",
            "gender": "N",
            "date_of_birth": "2021-01-01",
            "phone": "",
        },
    )
    assert response.status_code == 200
    assert response.data == {
        "id": 1,
        "email": "AdvIsoR_0@new-email.com",
        "first_name": "Test",
        "last_name": "Name",
        "gender": "N",
        "date_of_birth": "2021-01-01",
        "phone": "",
        "profile_photo": None,
    }


@pytest.mark.django_db
def test_update_stores_lowercase_email_as_username(
    mock_advisor_user,
    authenticated_api_client_as_advisor,
):
    response = authenticated_api_client_as_advisor.patch(
        f"/api/v1/advisors/{mock_advisor_user.id}/",
        {
            "email": "AdvIsoR_0@new-email.com",
        },
    )
    assert response.status_code == 200
    assert response.data["email"] == "AdvIsoR_0@new-email.com"

    assert Advisor.objects.filter(username="advisor_0@new-email.com").count() == 1


@pytest.mark.skip
def test_advisor_can_update_profile_photo():
    pass


@pytest.mark.django_db
def test_advisor_can_delete_self(
    mock_advisor_user,
    authenticated_api_client_as_advisor,
):
    response = authenticated_api_client_as_advisor.delete(
        f"/api/v1/advisors/{mock_advisor_user.id}/",
    )
    assert response.status_code == 204

    assert Advisor.objects.filter(id=mock_advisor_user.id).count() == 0
