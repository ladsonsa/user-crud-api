from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.exceptions.handlers import register_exception_handlers
from app.exceptions.user_exceptions import (
    AuthenticationError,
    UserNotFoundError,
)


def create_test_app() -> FastAPI:
    """Creates a temporary FastAPI instance registered with custom exception handlers for testing.

    Returns:
        FastAPI: The test application instance with custom routes that trigger exceptions.
    """
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/authentication-error")
    def authentication_error() -> None:
        raise AuthenticationError

    @app.get("/user-not-found")
    def user_not_found_error() -> None:
        raise UserNotFoundError

    return app


def test_authentication_error_handler_returns_401() -> None:
    """Tests that AuthenticationError yields an HTTP 401 response with the WWW-Authenticate header."""
    client = TestClient(create_test_app())

    response = client.get("/authentication-error")

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json() == {"detail": "Invalid authentication credentials"}


def test_user_not_found_handler_returns_404() -> None:
    """Tests that UserNotFoundError yields an HTTP 404 response with the expected detail message."""
    client = TestClient(create_test_app())

    response = client.get("/user-not-found")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
