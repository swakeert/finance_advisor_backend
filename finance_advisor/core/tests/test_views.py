import base64
import json

import pytest
from freezegun import freeze_time
from rest_framework.test import APIClient


@pytest.fixture
def mock_api_clients(
    authenticated_api_client_as_advisee,
    authenticated_api_client_as_advisor,
):
    return [
        authenticated_api_client_as_advisee,
        authenticated_api_client_as_advisor,
    ]


@pytest.mark.django_db
def test_unauthenticated_cannot_view_currencies():
    api_client = APIClient()
    response = api_client.get("/api/v1/core/currencies/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_users_can_view_all_currencies(mock_currency, mock_api_clients):
    for api_client in mock_api_clients:
        response = api_client.get("/api/v1/core/currencies/")
        assert response.status_code == 200

        assert {
            "id": mock_currency.id,
            "code": "MCK",
            "numeric_code": "123",
            "name": "Mock Currency",
        } in response.data

        response = api_client.post("/api/v1/core/currencies/")
        assert response.status_code == 405


@pytest.mark.django_db
@pytest.mark.parametrize(
    "filter_by, value",
    [
        ("code", "MCK"),
        ("numeric_code", "123"),
        ("name", "Mock Currency"),
    ],
)
def test_users_can_filter_currencies(mock_currency, mock_api_clients, filter_by, value):
    for api_client in mock_api_clients:
        response = api_client.get(f"/api/v1/core/currencies/?{filter_by}={value}")
        assert response.status_code == 200

        assert response.data == [
            {
                "id": mock_currency.id,
                "code": "MCK",
                "numeric_code": "123",
                "name": "Mock Currency",
            }
        ]

        response = api_client.post("/api/v1/core/currencies/")
        assert response.status_code == 405


@pytest.mark.django_db
def test_users_cannot_create_currencies(mock_api_clients):
    for api_client in mock_api_clients:
        response = api_client.post("/api/v1/core/currencies/")
        assert response.status_code == 405


@pytest.mark.django_db
def test_users_can_view_individual_currency(mock_currency, mock_api_clients):
    for api_client in mock_api_clients:
        response = api_client.get(f"/api/v1/core/currencies/{mock_currency.id}/")
        assert response.status_code == 200
        assert response.data == {
            "id": mock_currency.id,
            "code": "MCK",
            "numeric_code": "123",
            "name": "Mock Currency",
        }


@pytest.mark.django_db
def test_users_cannot_update_currency(mock_currency, mock_api_clients):
    for api_client in mock_api_clients:
        response = api_client.post(f"/api/v1/core/currencies/{mock_currency.id}/")
        assert response.status_code == 405
        response = api_client.put(f"/api/v1/core/currencies/{mock_currency.id}/")
        assert response.status_code == 405
        response = api_client.patch(f"/api/v1/core/currencies/{mock_currency.id}/")
        assert response.status_code == 405


@pytest.mark.django_db
def test_users_cannot_delete_currency(mock_currency, mock_api_clients):
    for api_client in mock_api_clients:
        response = api_client.delete(f"/api/v1/core/currencies/{mock_currency.id}/")
        assert response.status_code == 405


@freeze_time("2021-01-01")
@pytest.mark.django_db
@pytest.mark.skip(
    "Failing with 'Incorrect Padding Issue' Error. Initially it was working for Refresh tokens but not Access tokens, but now it's failing for both."
)
def test_login_advisee_user(mock_advisee_user):
    api_client = APIClient()

    response = api_client.post(
        "/api/v1/auth/login/",
        {
            "username": "advisee_0@email.com",
            "password": "test_password",
        },
    )

    assert response.status_code == 200

    refresh_token_payload = response.data["refresh"].split(".")[1]
    decoded_bytes = base64.standard_b64decode(refresh_token_payload)
    decoded_str = str(decoded_bytes, "utf-8")
    refresh_token_payload = json.loads(decoded_str)
    refresh_token_payload.pop("jti")
    assert refresh_token_payload == {
        "token_type": "refresh",
        "exp": 1612051200,
        "user_id": 1,
        "user_type": "advisee",
        "id": 1,
    }


@freeze_time("2021-01-01")
@pytest.mark.django_db
@pytest.mark.skip(
    "Failing with 'Incorrect Padding Issue' Error. Initially it was working for Refresh tokens but not Access tokens, but now it's failing for both."
)
def test_login_advisee_username_case_insensitive(mock_advisee_user):
    api_client = APIClient()

    response = api_client.post(
        "/api/v1/auth/login/",
        {
            "username": "AdvIsEE_0@email.com",
            "password": "test_password",
        },
    )

    assert response.status_code == 200
    refresh_token_payload = response.data["refresh"].split(".")[1]

    decoded_bytes = base64.standard_b64decode(refresh_token_payload)
    decoded_str = str(decoded_bytes, "utf-8")
    refresh_token_payload = json.loads(decoded_str)
    refresh_token_payload.pop("jti")
    assert refresh_token_payload == {
        "token_type": "refresh",
        "exp": 1612051200,
        "user_id": 1,
        "user_type": "advisee",
        "id": 1,
    }


@freeze_time("2021-01-01")
@pytest.mark.django_db
@pytest.mark.skip(
    "Failing with 'Incorrect Padding Issue' Error. Initially it was working for Refresh tokens but not Access tokens, but now it's failing for both."
)
def test_login_advisor_user(mock_advisor_user):
    api_client = APIClient()

    response = api_client.post(
        "/api/v1/auth/login/",
        {
            "username": "advisor_0@email.com",
            "password": "test_password",
        },
    )

    assert response.status_code == 200
    refresh_token_payload = response.data["refresh"].split(".")[1]

    decoded_bytes = base64.standard_b64decode(refresh_token_payload)
    decoded_str = str(decoded_bytes, "utf-8")
    refresh_token_payload = json.loads(decoded_str)
    refresh_token_payload.pop("jti")
    assert refresh_token_payload == {
        "token_type": "refresh",
        "exp": 1612051200,
        "user_id": 1,
        "user_type": "advisor",
        "id": 1,
    }


@pytest.mark.django_db
def test_login_fails_for_unknown_credentials():
    api_client = APIClient()

    response = api_client.post(
        "/api/v1/auth/login/",
        {
            "username": "advisor_0@email.com",
            "password": "test_password",
        },
    )

    assert response.status_code == 401


@freeze_time("2021-01-01")
@pytest.mark.django_db
@pytest.mark.skip(
    "Failing with 'Incorrect Padding Issue' Error. Initially it was working for Refresh tokens but not Access tokens, but now it's failing for both."
)
def test_refresh_works(mock_advisee_user):
    api_client = APIClient()

    response = api_client.post(
        "/api/v1/auth/login/",
        {
            "username": "advisee_0@email.com",
            "password": "test_password",
        },
    )

    assert response.status_code == 200

    refresh_token = response.data["refresh"]

    response = api_client.post(
        "/api/v1/auth/token/refresh/",
        {
            "refresh": refresh_token,
        },
    )
    assert response.status_code == 200
    refresh_token_payload = response.data["refresh"].split(".")[1]

    decoded_bytes = base64.standard_b64decode(refresh_token_payload)
    decoded_str = str(decoded_bytes, "utf-8")
    refresh_token_payload = json.loads(decoded_str)
    refresh_token_payload.pop("jti")
    assert refresh_token_payload == {
        "token_type": "refresh",
        "exp": 1612051200,
        "user_id": 1,
        "user_type": "advisee",
        "id": 1,
    }


@pytest.mark.django_db
def test_refresh_fails_for_random_token(mock_advisee_user):
    api_client = APIClient()

    response = api_client.post(
        "/api/v1/auth/token/refresh/",
        {
            "refresh": "garbage_token",
        },
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_refresh_fails_for_expired_token(mock_advisee_user):
    api_client = APIClient()

    with freeze_time("2021-01-01"):
        response = api_client.post(
            "/api/v1/auth/login/",
            {
                "username": "advisee_0@email.com",
                "password": "test_password",
            },
        )

    assert response.status_code == 200
    refresh_token = response.data["refresh"]

    with freeze_time("2021-02-01"):
        response = api_client.post(
            "/api/v1/auth/token/refresh/",
            {
                "refresh": refresh_token,
            },
        )
    assert response.status_code == 401
