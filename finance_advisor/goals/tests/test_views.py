from collections import OrderedDict

import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_unauthenticated_cannot_perform_goal_actions(mock_advisee_user):
    api_client = APIClient()
    response = api_client.get(f"/api/v1/advisees/{mock_advisee_user.id}/goals/")
    assert response.status_code == 403
    response = api_client.put(f"/api/v1/advisees/{mock_advisee_user.id}/goals/")
    assert response.status_code == 403
    response = api_client.post(f"/api/v1/advisees/{mock_advisee_user.id}/goals/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_advisee_can_list_their_goals(
    mock_advisee_user,
    mock_currency,
    mock_goal,
    authenticated_api_client_as_advisee,
):
    response = authenticated_api_client_as_advisee.get(
        f"/api/v1/advisees/{mock_advisee_user.id}/goals/"
    )
    assert response.status_code == 200
    assert response.data == [
        OrderedDict(
            {
                "id": 1,
                "name": "Goal 0",
                "value": 0,
                "currency": mock_currency.id,
                "target_date": "2021-01-01",
            }
        )
    ]


@pytest.mark.django_db
def test_advisee_can_create_new_goals(
    mock_advisee_user,
    mock_currency,
    authenticated_api_client_as_advisee,
):
    response = authenticated_api_client_as_advisee.post(
        f"/api/v1/advisees/{mock_advisee_user.id}/goals/",
        {
            "name": "New Goal",
            "value": 100,
            "currency": mock_currency.id,
            "target_date": "2009-01-01",
        },
    )

    assert response.status_code == 201
    assert response.data == {
        "id": 1,
        "name": "New Goal",
        "value": 100,
        "currency": mock_currency.id,
        "target_date": "2009-01-01",
    }


@pytest.mark.django_db
def test_advisee_can_view_their_individual_goals(
    mock_advisee_user,
    mock_currency,
    mock_goal,
    authenticated_api_client_as_advisee,
):
    response = authenticated_api_client_as_advisee.get(
        f"/api/v1/advisees/{mock_advisee_user.id}/goals/{mock_goal.id}/"
    )
    assert response.status_code == 200
    assert response.data == {
        "id": mock_goal.id,
        "name": "Goal 0",
        "value": 0,
        "currency": mock_currency.id,
        "target_date": "2021-01-01",
    }


@pytest.mark.django_db
def test_advisee_can_update_their_individual_goals(
    mock_advisee_user,
    mock_currency,
    mock_alternate_currency,
    mock_goal,
    authenticated_api_client_as_advisee,
):
    response = authenticated_api_client_as_advisee.patch(
        f"/api/v1/advisees/{mock_advisee_user.id}/goals/{mock_goal.id}/",
        {
            "name": "Goal 001",
            "value": 10,
        },
    )
    assert response.status_code == 200
    assert response.data == {
        "id": mock_goal.id,
        "name": "Goal 001",
        "value": 10,
        "currency": mock_currency.id,
        "target_date": "2021-01-01",
    }

    response = authenticated_api_client_as_advisee.put(
        f"/api/v1/advisees/{mock_advisee_user.id}/goals/{mock_goal.id}/",
        {
            "name": "Goal 10001",
            "value": 1000,
            "currency": mock_alternate_currency.id,
            "target_date": "2021-01-01",
        },
    )
    assert response.status_code == 200
    assert response.data == {
        "id": mock_goal.id,
        "name": "Goal 10001",
        "value": 1000,
        "currency": mock_alternate_currency.id,
        "target_date": "2021-01-01",
    }


@pytest.mark.django_db
def test_advisee_can_delete_their_individual_goals(
    mock_advisee_user,
    mock_goal,
    authenticated_api_client_as_advisee,
):
    response = authenticated_api_client_as_advisee.delete(
        f"/api/v1/advisees/{mock_advisee_user.id}/goals/{mock_goal.id}/"
    )
    assert response.status_code == 204


@pytest.mark.django_db
def test_advisee_cannot_CRUD_other_advisee_goals(
    mock_alternate_advisee_user,
    mock_alternate_users_goal,
    authenticated_api_client_as_advisee,
):
    response = authenticated_api_client_as_advisee.get(
        f"/api/v1/advisees/{mock_alternate_advisee_user.id}/goals/"
    )
    assert response.status_code == 403

    response = authenticated_api_client_as_advisee.post(
        f"/api/v1/advisees/{mock_alternate_advisee_user.id}/goals/"
    )
    assert response.status_code == 403

    response = authenticated_api_client_as_advisee.get(
        f"/api/v1/advisees/{mock_alternate_advisee_user.id}/goals/{mock_alternate_users_goal.id}/"
    )
    assert response.status_code == 403

    response = authenticated_api_client_as_advisee.put(
        f"/api/v1/advisees/{mock_alternate_advisee_user.id}/goals/{mock_alternate_users_goal.id}/"
    )
    assert response.status_code == 403

    response = authenticated_api_client_as_advisee.delete(
        f"/api/v1/advisees/{mock_alternate_advisee_user.id}/goals/{mock_alternate_users_goal.id}/"
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_advisor_can_list_client_goals(
    mock_advisee_user,
    mock_goal,
    authenticated_api_client_as_advisor,
    mock_relationship,
    mock_currency,
):
    response = authenticated_api_client_as_advisor.get(
        f"/api/v1/advisees/{mock_advisee_user.id}/goals/"
    )
    assert response.status_code == 200
    assert response.data == [
        OrderedDict(
            {
                "id": 1,
                "name": "Goal 0",
                "value": 0,
                "currency": mock_currency.id,
                "target_date": "2021-01-01",
            }
        )
    ]


@pytest.mark.django_db
def test_advisor_can_create_client_goals(
    mock_advisee_user,
    authenticated_api_client_as_advisor,
    mock_relationship,
    mock_currency,
):
    response = authenticated_api_client_as_advisor.post(
        f"/api/v1/advisees/{mock_advisee_user.id}/goals/",
        {
            "name": "New Goal",
            "value": 100,
            "currency": mock_currency.id,
            "target_date": "2009-01-01",
        },
    )

    assert response.status_code == 201
    assert response.data == {
        "id": 1,
        "name": "New Goal",
        "value": 100,
        "currency": mock_currency.id,
        "target_date": "2009-01-01",
    }


@pytest.mark.django_db
def test_advisor_can_view_client_individual_goal(
    mock_advisee_user,
    mock_goal,
    authenticated_api_client_as_advisor,
    mock_relationship,
    mock_currency,
):
    response = authenticated_api_client_as_advisor.get(
        f"/api/v1/advisees/{mock_advisee_user.id}/goals/{mock_goal.id}/"
    )
    assert response.status_code == 200
    assert response.data == {
        "id": 1,
        "name": "Goal 0",
        "value": 0,
        "currency": mock_currency.id,
        "target_date": "2021-01-01",
    }


@pytest.mark.django_db
def test_advisor_can_update_client_individual_goal(
    mock_advisee_user,
    mock_goal,
    authenticated_api_client_as_advisor,
    mock_relationship,
    mock_currency,
    mock_alternate_currency,
):
    response = authenticated_api_client_as_advisor.patch(
        f"/api/v1/advisees/{mock_advisee_user.id}/goals/{mock_goal.id}/",
        {
            "name": "Goal 001",
            "value": 10,
        },
    )
    assert response.status_code == 200
    assert response.data == {
        "id": mock_goal.id,
        "name": "Goal 001",
        "value": 10,
        "currency": mock_currency.id,
        "target_date": "2021-01-01",
    }

    response = authenticated_api_client_as_advisor.put(
        f"/api/v1/advisees/{mock_advisee_user.id}/goals/{mock_goal.id}/",
        {
            "name": "Goal 10001",
            "value": 1000,
            "currency": mock_alternate_currency.id,
            "target_date": "2021-01-01",
        },
    )
    assert response.status_code == 200
    assert response.data == {
        "id": mock_goal.id,
        "name": "Goal 10001",
        "value": 1000,
        "currency": mock_alternate_currency.id,
        "target_date": "2021-01-01",
    }


@pytest.mark.django_db
def test_advisor_can_delete_client_individual_goal(
    mock_advisee_user,
    mock_goal,
    authenticated_api_client_as_advisor,
    mock_relationship,
):
    response = authenticated_api_client_as_advisor.delete(
        f"/api/v1/advisees/{mock_advisee_user.id}/goals/{mock_goal.id}/"
    )
    assert response.status_code == 204


@pytest.mark.django_db
def test_advisor_cannot_CRUD_non_client_advisee_goals(
    mock_alternate_advisee_user,
    mock_alternate_users_goal,
    authenticated_api_client_as_advisor,
):
    response = authenticated_api_client_as_advisor.get(
        f"/api/v1/advisees/{mock_alternate_advisee_user.id}/goals/"
    )
    assert response.status_code == 403

    response = authenticated_api_client_as_advisor.post(
        f"/api/v1/advisees/{mock_alternate_advisee_user.id}/goals/"
    )
    assert response.status_code == 403

    response = authenticated_api_client_as_advisor.get(
        f"/api/v1/advisees/{mock_alternate_advisee_user.id}/goals/{mock_alternate_users_goal.id}/"
    )
    assert response.status_code == 403

    response = authenticated_api_client_as_advisor.put(
        f"/api/v1/advisees/{mock_alternate_advisee_user.id}/goals/{mock_alternate_users_goal.id}/"
    )
    assert response.status_code == 403

    response = authenticated_api_client_as_advisor.delete(
        f"/api/v1/advisees/{mock_alternate_advisee_user.id}/goals/{mock_alternate_users_goal.id}/"
    )
    assert response.status_code == 403
