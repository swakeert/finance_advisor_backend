from collections import OrderedDict

import pytest
from rest_framework.test import APIClient

from finance_advisor.cash_flows.models import Income


@pytest.mark.django_db
def test_unauthenticated_cannot_perform_income_actions(mock_advisee_user):
    api_client = APIClient()
    response = api_client.get(f"/api/v1/advisees/{mock_advisee_user.id}/incomes/")
    assert response.status_code == 401
    response = api_client.put(f"/api/v1/advisees/{mock_advisee_user.id}/incomes/")
    assert response.status_code == 401
    response = api_client.post(f"/api/v1/advisees/{mock_advisee_user.id}/incomes/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_advisee_can_list_their_incomes(
    mock_advisee_user,
    mock_currency,
    mock_income,
    mock_income_type,
    authenticated_api_client_as_advisee,
):
    response = authenticated_api_client_as_advisee.get(
        f"/api/v1/advisees/{mock_advisee_user.id}/incomes/"
    )
    assert response.status_code == 200
    assert response.data == [
        OrderedDict(
            {
                "id": 1,
                "annual_value": 1000,
                "currency": mock_currency.id,
                "income_type": mock_income_type.id,
                "notes": "My first salary",
            }
        )
    ]


@pytest.mark.django_db
def test_advisee_can_create_new_incomes(
    mock_advisee_user,
    mock_currency,
    mock_income_type,
    authenticated_api_client_as_advisee,
):
    response = authenticated_api_client_as_advisee.post(
        f"/api/v1/advisees/{mock_advisee_user.id}/incomes/",
        {
            "annual_value": 100,
            "currency": mock_currency.id,
            "income_type": mock_income_type.id,
            "notes": "New source of income",
        },
    )

    assert response.status_code == 201
    assert response.data == {
        "id": 1,
        "annual_value": 100,
        "currency": mock_currency.id,
        "income_type": mock_income_type.id,
        "notes": "New source of income",
    }


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field, incorrect_value, error_msg",
    [
        ("annual_value", -1, "Ensure this value is greater than or equal to 0."),
        ("annual_value", "", "A valid integer is required."),
        ("annual_value", "null", "A valid integer is required."),
        ("currency", -1, 'Invalid pk "-1" - object does not exist.'),
        ("currency", "", "This field may not be null."),
        ("income_type", -1, 'Invalid pk "-1" - object does not exist.'),
    ],
)
def test_income_validations(
    mock_advisee_user,
    mock_income,
    authenticated_api_client_as_advisee,
    field,
    incorrect_value,
    error_msg,
):
    response = authenticated_api_client_as_advisee.patch(
        f"/api/v1/advisees/{mock_advisee_user.id}/incomes/{mock_income.id}/",
        {field: incorrect_value},
    )

    assert response.status_code == 400
    assert response.data[field][0] == error_msg


@pytest.mark.django_db
def test_advisee_can_view_their_incomes_individually(
    mock_advisee_user,
    mock_currency,
    mock_income,
    mock_income_type,
    authenticated_api_client_as_advisee,
):
    response = authenticated_api_client_as_advisee.get(
        f"/api/v1/advisees/{mock_advisee_user.id}/incomes/{mock_income.id}/"
    )
    assert response.status_code == 200
    assert response.data == {
        "id": 1,
        "annual_value": 1000,
        "currency": mock_currency.id,
        "income_type": mock_income_type.id,
        "notes": "My first salary",
    }


@pytest.mark.django_db
def test_advisee_can_update_their_incomes_individually(
    mock_advisee_user,
    mock_currency,
    mock_alternate_currency,
    mock_income,
    mock_income_type,
    mock_alternate_income_type,
    authenticated_api_client_as_advisee,
):
    response = authenticated_api_client_as_advisee.patch(
        f"/api/v1/advisees/{mock_advisee_user.id}/incomes/{mock_income.id}/",
        {
            "annual_value": 10,
            "notes": "My second salary",
        },
    )
    assert response.status_code == 200
    assert response.data == {
        "id": 1,
        "annual_value": 10,
        "currency": mock_currency.id,
        "income_type": mock_income_type.id,
        "notes": "My second salary",
    }

    response = authenticated_api_client_as_advisee.put(
        f"/api/v1/advisees/{mock_advisee_user.id}/incomes/{mock_income.id}/",
        {
            "annual_value": 0,
            "currency": mock_alternate_currency.id,
            "income_type": mock_alternate_income_type.id,
            "notes": "My last salary",
        },
    )
    assert response.status_code == 200
    assert response.data == {
        "id": mock_income.id,
        "annual_value": 0,
        "currency": mock_alternate_currency.id,
        "income_type": mock_alternate_income_type.id,
        "notes": "My last salary",
    }


@pytest.mark.django_db
def test_advisee_can_delete_their_incomes_individually(
    mock_advisee_user,
    mock_income,
    authenticated_api_client_as_advisee,
):
    response = authenticated_api_client_as_advisee.delete(
        f"/api/v1/advisees/{mock_advisee_user.id}/incomes/{mock_income.id}/"
    )
    assert response.status_code == 204
    assert Income.objects.filter(id=mock_income.id).count() == 0


@pytest.mark.django_db
def test_advisee_delete_cascades(
    mock_advisee_user,
    mock_income,
    authenticated_api_client_as_advisee,
):
    response = authenticated_api_client_as_advisee.delete(
        f"/api/v1/advisees/{mock_advisee_user.id}/"
    )
    assert response.status_code == 204
    assert Income.objects.filter(id=mock_income.id).count() == 0


@pytest.mark.django_db
def test_advisee_cannot_CRUD_other_advisee_incomes(
    mock_alternate_advisee_user,
    mock_alternate_users_income,
    authenticated_api_client_as_advisee,
):
    response = authenticated_api_client_as_advisee.get(
        f"/api/v1/advisees/{mock_alternate_advisee_user.id}/incomes/"
    )
    assert response.status_code == 403

    response = authenticated_api_client_as_advisee.post(
        f"/api/v1/advisees/{mock_alternate_advisee_user.id}/incomes/"
    )
    assert response.status_code == 403

    response = authenticated_api_client_as_advisee.get(
        f"/api/v1/advisees/{mock_alternate_advisee_user.id}/incomes/{mock_alternate_users_income.id}/"
    )
    assert response.status_code == 403

    response = authenticated_api_client_as_advisee.put(
        f"/api/v1/advisees/{mock_alternate_advisee_user.id}/incomes/{mock_alternate_users_income.id}/"
    )
    assert response.status_code == 403

    response = authenticated_api_client_as_advisee.delete(
        f"/api/v1/advisees/{mock_alternate_advisee_user.id}/incomes/{mock_alternate_users_income.id}/"
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_advisor_can_list_client_incomes(
    mock_advisee_user,
    mock_income,
    mock_income_type,
    authenticated_api_client_as_advisor,
    mock_relationship,
    mock_currency,
):
    response = authenticated_api_client_as_advisor.get(
        f"/api/v1/advisees/{mock_advisee_user.id}/incomes/"
    )
    assert response.status_code == 200
    assert response.data == [
        OrderedDict(
            {
                "id": 1,
                "annual_value": 1000,
                "currency": mock_currency.id,
                "income_type": mock_income_type.id,
                "notes": "My first salary",
            }
        )
    ]


@pytest.mark.django_db
def test_advisor_can_create_client_incomes(
    mock_advisee_user,
    authenticated_api_client_as_advisor,
    mock_relationship,
    mock_income_type,
    mock_currency,
):
    response = authenticated_api_client_as_advisor.post(
        f"/api/v1/advisees/{mock_advisee_user.id}/incomes/",
        {
            "annual_value": 100,
            "currency": mock_currency.id,
            "income_type": mock_income_type.id,
            "notes": "New source of income",
        },
    )

    assert response.status_code == 201
    assert response.data == {
        "id": 1,
        "annual_value": 100,
        "currency": mock_currency.id,
        "income_type": mock_income_type.id,
        "notes": "New source of income",
    }


@pytest.mark.django_db
def test_advisor_can_view_client_income_individually(
    mock_advisee_user,
    mock_income,
    mock_income_type,
    authenticated_api_client_as_advisor,
    mock_relationship,
    mock_currency,
):
    response = authenticated_api_client_as_advisor.get(
        f"/api/v1/advisees/{mock_advisee_user.id}/incomes/{mock_income.id}/"
    )
    assert response.status_code == 200
    assert response.data == {
        "id": 1,
        "annual_value": 1000,
        "currency": mock_currency.id,
        "income_type": mock_income_type.id,
        "notes": "My first salary",
    }


@pytest.mark.django_db
def test_advisor_can_update_client_income_individually(
    mock_advisee_user,
    mock_currency,
    mock_alternate_currency,
    mock_income,
    mock_income_type,
    mock_alternate_income_type,
    authenticated_api_client_as_advisor,
    mock_relationship,
):
    response = authenticated_api_client_as_advisor.patch(
        f"/api/v1/advisees/{mock_advisee_user.id}/incomes/{mock_income.id}/",
        {
            "annual_value": 10,
            "notes": "My second salary",
        },
    )
    assert response.status_code == 200
    assert response.data == {
        "id": 1,
        "annual_value": 10,
        "currency": mock_currency.id,
        "income_type": mock_income_type.id,
        "notes": "My second salary",
    }

    response = authenticated_api_client_as_advisor.put(
        f"/api/v1/advisees/{mock_advisee_user.id}/incomes/{mock_income.id}/",
        {
            "annual_value": 0,
            "currency": mock_alternate_currency.id,
            "income_type": mock_alternate_income_type.id,
            "notes": "My last salary",
        },
    )
    assert response.status_code == 200
    assert response.data == {
        "id": mock_income.id,
        "annual_value": 0,
        "currency": mock_alternate_currency.id,
        "income_type": mock_alternate_income_type.id,
        "notes": "My last salary",
    }


@pytest.mark.django_db
def test_advisor_can_delete_client_income_individually(
    mock_advisee_user,
    mock_income,
    authenticated_api_client_as_advisor,
    mock_relationship,
):
    response = authenticated_api_client_as_advisor.delete(
        f"/api/v1/advisees/{mock_advisee_user.id}/incomes/{mock_income.id}/"
    )
    assert response.status_code == 204
    assert Income.objects.filter(id=mock_income.id).count() == 0


@pytest.mark.django_db
def test_advisor_cannot_CRUD_non_client_advisee_incomes(
    mock_alternate_advisee_user,
    mock_alternate_users_income,
    authenticated_api_client_as_advisor,
):
    response = authenticated_api_client_as_advisor.get(
        f"/api/v1/advisees/{mock_alternate_advisee_user.id}/incomes/"
    )
    assert response.status_code == 403

    response = authenticated_api_client_as_advisor.post(
        f"/api/v1/advisees/{mock_alternate_advisee_user.id}/incomes/"
    )
    assert response.status_code == 403

    response = authenticated_api_client_as_advisor.get(
        f"/api/v1/advisees/{mock_alternate_advisee_user.id}/incomes/{mock_alternate_users_income.id}/"
    )
    assert response.status_code == 403

    response = authenticated_api_client_as_advisor.put(
        f"/api/v1/advisees/{mock_alternate_advisee_user.id}/incomes/{mock_alternate_users_income.id}/"
    )
    assert response.status_code == 403

    response = authenticated_api_client_as_advisor.delete(
        f"/api/v1/advisees/{mock_alternate_advisee_user.id}/incomes/{mock_alternate_users_income.id}/"
    )
    assert response.status_code == 403
