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
    print(response.status_code)
    print(response.json())
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
