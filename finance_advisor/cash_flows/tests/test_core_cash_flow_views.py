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
def test_unauthenticated_cannot_view_core_incomes():
    api_client = APIClient()
    response = api_client.get("/api/v1/core/incomes/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_users_can_view_all_cash_flows(
    mock_income_category, mock_income_type, mock_api_clients
):
    for api_client in mock_api_clients:
        response = api_client.get("/api/v1/core/incomes/")
        assert response.status_code == 200

        assert {
            "id": mock_income_category.id,
            "name": "Income Category 1",
            "income_types": [
                {
                    "id": mock_income_type.id,
                    "name": "Income Type 1",
                },
            ],
        } in response.data

        response = api_client.post("/api/v1/core/incomes/")
        assert response.status_code == 405


@pytest.mark.django_db
def test_users_cannot_create_incomes(mock_api_clients):
    for api_client in mock_api_clients:
        response = api_client.post("/api/v1/core/incomes/")
        assert response.status_code == 405


@pytest.mark.django_db
def test_users_cannot_view_individual_income_category(
    mock_income_category, mock_api_clients
):
    for api_client in mock_api_clients:
        response = api_client.get(f"/api/v1/core/incomes/{mock_income_category.id}/")
        assert response.status_code == 404
