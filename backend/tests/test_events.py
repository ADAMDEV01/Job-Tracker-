from fastapi.testclient import TestClient

from tests.test_applications import authenticated_headers, create_application


def test_create_and_update_write_ordered_application_history(
    client: TestClient,
) -> None:
    headers = authenticated_headers(client, "person@example.com")
    application = create_application(client, headers)
    application_id = application["id"]

    updated = client.patch(
        f"/applications/{application_id}",
        headers=headers,
        json={"status": "replied"},
    )
    assert updated.status_code == 200
    client.patch(
        f"/applications/{application_id}",
        headers=headers,
        json={"notes": "Recruiter called"},
    )

    response = client.get(
        f"/applications/{application_id}/events",
        headers=headers,
    )

    assert response.status_code == 200
    events = response.json()
    assert [event["event_type"] for event in events] == [
        "created",
        "status_changed",
        "updated",
    ]
    assert events[0]["previous_status"] is None
    assert events[0]["new_status"] == "applied"
    assert events[1]["previous_status"] == "applied"
    assert events[1]["new_status"] == "replied"
    assert events[2]["previous_status"] == events[2]["new_status"] == "replied"


def test_events_are_private_to_application_owner(client: TestClient) -> None:
    owner_headers = authenticated_headers(client, "owner@example.com")
    other_headers = authenticated_headers(client, "other@example.com")
    application = create_application(client, owner_headers)

    response = client.get(
        f"/applications/{application['id']}/events",
        headers=other_headers,
    )

    assert response.status_code == 404


def test_events_require_authentication(client: TestClient) -> None:
    response = client.get("/applications/1/events")

    assert response.status_code == 401
