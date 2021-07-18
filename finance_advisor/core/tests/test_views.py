import pytest
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
    assert response.status_code == 403


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
