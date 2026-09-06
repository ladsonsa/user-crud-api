from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient

from app.database.init_db import init_database
from app.main import app

client = TestClient(app)


def create_authenticated_user(
    name: str,
    email: str,
) -> tuple[int, dict[str, str]]:
    """Registers a new user and authenticates them to retrieve authorization headers for integration tests.

    Executes a POST request to `/api/v1/users` to create a test user, followed by a POST request
    to `/api/v1/auth/login` to obtain an access token. Asserts success on both operations.

    Args:
        name (str): The full name of the user to register.
        email (str): The email address for account creation and login.

    Returns:
        tuple[int, dict[str, str]]: A tuple containing:
            - int: The created user's ID.
            - dict[str, str]: A dictionary containing the HTTP `Authorization` Bearer token header.
    """
    response = client.post(
        "/api/v1/users",
        json={
            "name": name,
            "email": email,
            "password": "SecurePassword123",
        },
    )
    assert response.status_code == 201

    user_id = response.json()["id"]

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": "SecurePassword123",
        },
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return user_id, {"Authorization": f"Bearer {token}"}


def setup_module() -> None:
    """Prepares the test module environment by initializing the database schema."""
    init_database()


def test_create_user() -> None:
    """Tests successful user registration with a valid payload returning HTTP 201 Created."""
    response = client.post(
        "/api/v1/users",
        json={
            "name": "Alice",
            "email": "alice.routes@example.com",
            "password": "SecurePassword123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Alice"
    assert data["email"] == "alice.routes@example.com"
    assert "id" in data


def test_list_users() -> None:
    """Tests the authenticated endpoint for retrieving a list of all existing users."""
    _, headers = create_authenticated_user(
        "List User",
        "list.routes@example.com",
    )

    response = client.get(
        "/api/v1/users",
        headers=headers,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user() -> None:
    """Tests retrieving a specific user by identifier via the API endpoint."""
    user_id, headers = create_authenticated_user(
        "Bob",
        "bob.routes@example.com",
    )

    response = client.get(
        f"/api/v1/users/{user_id}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == user_id


def test_update_user() -> None:
    """Tests updating an existing user's details via the API endpoint."""
    user_id, headers = create_authenticated_user(
        "Carol",
        "carol.routes@example.com",
    )

    response = client.put(
        f"/api/v1/users/{user_id}",
        headers=headers,
        json={
            "name": "Carol Updated",
            "email": "carol.updated.routes@example.com",
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Carol Updated"


def test_delete_user() -> None:
    """Tests deleting a user via the API endpoint and ensuring subsequent access is restricted."""
    user_id, user_headers = create_authenticated_user(
        "Dave",
        "dave.routes@example.com",
    )

    response = client.delete(
        f"/api/v1/users/{user_id}",
        headers=user_headers,
    )

    assert response.status_code == 204

    _, admin_headers = create_authenticated_user(
        "Admin",
        "admin.routes@example.com",
    )

    response = client.get(
        f"/api/v1/users/{user_id}",
        headers=admin_headers,
    )

    assert response.status_code == 403


def test_update_user_with_empty_payload() -> None:
    """Tests that submitting an empty update payload results in an HTTP 422 Unprocessable Entity error."""
    user_id, headers = create_authenticated_user(
        "Eve",
        "eve.routes@example.com",
    )

    response = client.put(
        f"/api/v1/users/{user_id}",
        json={},
        headers=headers,
    )

    assert response.status_code == 422


def test_create_user_duplicate_email() -> None:
    """Tests that attempting to register two users with the same email address returns an HTTP 409 Conflict error."""
    payload = {
        "name": "Duplicate",
        "email": "duplicate.routes@example.com",
        "password": "SecurePassword123",
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
    """Tests user registration with various invalid payloads to ensure validation triggers HTTP 422 errors.

    Args:
        payload (dict[str, object]): Invalid request payload parameter supplied by pytest matrix.
    """
    response = client.post("/api/v1/users", json=payload)

    assert response.status_code == 422


def test_get_user_not_found() -> None:
    """Tests retrieving a nonexistent user ID, ensuring access controls or masking return HTTP 403 Forbidden."""
    _, headers = create_authenticated_user(
        "Not Found",
        "not-found.routes@example.com",
    )

    response = client.get(
        "/api/v1/users/999999",
        headers=headers,
    )

    assert response.status_code == 403


@pytest.mark.parametrize("user_id", ["invalid", "abc", "1.5"])
def test_get_user_invalid_id(user_id: str) -> None:
    """Tests that fetching a user with a non-integer or malformed path parameter returns an HTTP 422 error.

    Args:
        user_id (str): Invalid user identifier parameter supplied by pytest matrix.
    """
    _, headers = create_authenticated_user(
        "Invalid ID",
        "invalid-id.routes@example.com",
    )

    response = client.get(
        f"/api/v1/users/{user_id}",
        headers=headers,
    )

    assert response.status_code == 422


def test_update_user_duplicate_email() -> None:
    """Tests updating a user's email to one already registered by another user, verifying HTTP 409 Conflict."""
    first_id, _ = create_authenticated_user(
        "First",
        "first.update@example.com",
    )

    second_id, second_headers = create_authenticated_user(
        "second",
        "second.update@example.com",
    )

    response = client.put(
        f"/api/v1/users/{second_id}",
        headers=second_headers,
        json={
            "name": "Second Updated",
            "email": "first.update@example.com",
        },
    )

    assert response.status_code == 409


def test_update_user_not_found() -> None:
    """Tests updating a nonexistent user ID, verifying access controls return HTTP 403 Forbidden."""
    _, headers = create_authenticated_user(
        "Found",
        "fount@example.com",
    )

    response = client.put(
        "/api/v1/users/999999",
        headers=headers,
        json={
            "name": "Not Found",
            "email": "not-found.update@example.com",
        },
    )

    assert response.status_code == 403


def test_delete_user_not_found() -> None:
    """Tests deleting a nonexistent user ID, verifying access controls return HTTP 403 Forbidden."""
    _, headers = create_authenticated_user(
        "Delete",
        "delete@example.com",
    )
    response = client.delete(
        "/api/v1/users/999999",
        headers=headers,
    )

    assert response.status_code == 403


def test_create_user_concurrent_duplicate_email() -> None:
    """Tests race conditions when creating users concurrently with identical email addresses."""

    def create_user() -> int:
        """Sends a POST request to create a user with a duplicate email payload.

        Returns:
            int: The HTTP status code returned by the user creation endpoint.
        """
        response = client.post(
            "/api/v1/users",
            json={
                "name": "Concurrent User",
                "email": "concurrent@example.com",
                "password": "SecurePassword123",
            },
        )

        return response.status_code

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _: create_user(), range(2)))

    assert sorted(results) == [201, 409]


@pytest.mark.parametrize(
    "user_id",
    [
        "99999999999999999999999999999999",
        "abc",
        "1.5",
    ],
)
def test_get_user_user_id_invalid(user_id: str) -> None:
    """Tests that passing invalid user_id path parameters returns an HTTP 422 Unprocessable Entity error.

    Args:
        user_id (str): Malformed user ID path parameter supplied by pytest matrix.
    """
    _, headers = create_authenticated_user(
        "Get invalid ID",
        "get-invalid-id.routes@example.com",
    )
    response = client.get(
        f"/api/v1/users/{user_id}",
        headers=headers,
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    ("user_id", "expected_status"),
    [
        ("999999999", 403),
        ("abc", 422),
    ],
)
def test_update_user_invalid_user_id(
    user_id: str,
    expected_status: int,
) -> None:
    """Tests updating a user with nonexistent or malformed path parameters.

    Args:
        user_id (str): Path parameter under test.
        expected_status (int): Expected HTTP status code corresponding to the path parameter.
    """
    _, headers = create_authenticated_user(
        "Put invalid ID",
        "put-invalid-id.routes@example.com",
    )
    response = client.put(
        f"/api/v1/users/{user_id}",
        headers=headers,
        json={
            "name": "Updated User",
            "email": "updated@example.com",
        },
    )

    assert response.status_code == expected_status
