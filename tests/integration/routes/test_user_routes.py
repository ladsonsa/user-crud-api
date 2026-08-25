import pytest
from fastapi.testclient import TestClient

from app.database.init_db import init_database
from app.main import app

client = TestClient(app)


def setup_module() -> None:
    """Prepares the test module environment by initializing the database schema."""
    init_database()


def test_create_user() -> None:
    """Tests the user creation endpoint with valid payload."""
    response = client.post(
        "/api/v1/users",
        json={
            "name": "Alice",
            "email": "alice.routes@example.com",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Alice"
    assert data["email"] == "alice.routes@example.com"
    assert "id" in data


def test_list_users() -> None:
    """Tests the endpoint for listing all existing users."""
    response = client.get("/api/v1/users")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user() -> None:
    """Tests retrieving a specific user by identifier via API endpoint."""
    created = client.post(
        "/api/v1/users",
        json={
            "name": "Bob",
            "email": "bob.routes@example.com",
        },
    ).json()

    response = client.get(f"/api/v1/users/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_update_user() -> None:
    """Tests updating an existing user record via API endpoint."""
    created = client.post(
        "/api/v1/users",
        json={
            "name": "Carol",
            "email": "carol.routes@example.com",
        },
    ).json()

    response = client.put(
        f"/api/v1/users/{created['id']}",
        json={
            "name": "Carol Updated",
            "email": "carol.updated.routes@example.com",
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Carol Updated"


def test_delete_user() -> None:
    """Tests deleting a user via API endpoint and verifying its subsequent absence."""
    created = client.post(
        "/api/v1/users",
        json={
            "name": "Dave",
            "email": "dave.routes@example.com",
        },
    ).json()

    response = client.delete(f"/api/v1/users/{created['id']}")

    assert response.status_code == 204

    response = client.get(f"/api/v1/users/{created['id']}")

    assert response.status_code == 404


def test_update_user_with_empty_payload() -> None:
    """Tests that an empty update payload is rejected by the API."""

    created = client.post(
        "/api/v1/users",
        json={
            "name": "Eve",
            "email": "eve.routes@example.com",
        },
    ).json()

    response = client.put(
        f"/api/v1/users/{created['id']}",
        json={},
    )

    assert response.status_code == 422


def test_create_user_duplicate_email() -> None:
    payload = {
        "name": "Duplicate",
        "email": "duplicate.routes@example.com",
    }

    first_response = client.post("/api/v1/users", json=payload)
    second_response = client.post("/api/v1/users", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409


@pytest.mark.parametrize(
    "payload",
    [
        {"email": "missing-name@example.com"},
        {"name": "Missing Email"},
        {"name": None, "email": "null-name@example.com"},
        {"name": "Null Email", "email": None},
        {"name": "", "email": "empty-name@example.com"},
        {"name": "Invalid Email", "email": "invalid-email"},
        {"name": 123, "email": "invalid-type@example.com"},
        {
            "name": "Extra Field",
            "email": "extra-field@example.com",
            "extra": "forbidden",
        },
        {
            "name": "A" * 101,
            "email": "long-name@example.com",
        },
    ],
)
def test_create_user_invalid_payload(payload: dict[str, object]) -> None:
    response = client.post("/api/v1/users", json=payload)

    assert response.status_code == 422


def test_get_user_not_found() -> None:
    response = client.get("/api/v1/users/999999")

    assert response.status_code == 404


@pytest.mark.parametrize("user_id", ["invalid", "abc", "1.5"])
def test_get_user_invalid_id(user_id: str) -> None:
    response = client.get(f"/api/v1/users/{user_id}")

    assert response.status_code == 422


def test_update_user_duplicate_email() -> None:
    first = client.post(
        "/api/v1/users",
        json={
            "name": "First",
            "email": "first.update@example.com",
        },
    ).json()

    second = client.post(
        "/api/v1/users",
        json={
            "name": "Second",
            "email": "second.update@example.com",
        },
    ).json()

    response = client.put(
        f"/api/v1/users/{second['id']}",
        json={
            "name": "Second Updated",
            "email": first["email"],
        },
    )

    assert response.status_code == 409


def test_update_user_not_found() -> None:
    response = client.put(
        "/api/v1/users/999999",
        json={
            "name": "Not Found",
            "email": "not-found.update@example.com",
        },
    )

    assert response.status_code == 404


def test_delete_user_not_found() -> None:
    response = client.delete("/api/v1/users/999999")

    assert response.status_code == 404
