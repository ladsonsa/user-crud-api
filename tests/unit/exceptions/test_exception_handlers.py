from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.exceptions.handlers import register_exception_handlers
from app.exceptions.user_exceptions import DatabaseOperationError


def create_test_app() -> FastAPI:
    """Creates and configures a FastAPI application instance for testing exception handlers.

    Returns:
        FastAPI: A configured FastAPI test application with registered exception routes.
    """
    test_app = FastAPI()
    register_exception_handlers(test_app)

    @test_app.get("/database-error")
    async def database_error() -> None:
        """Simulates an endpoint that raises a DatabaseOperationError.

        Raises:
            DatabaseOperationError: Always raised to test database exception handling.
        """
        raise DatabaseOperationError

    @test_app.get("/unexpected-error")
    async def unexpected_error() -> None:
        """Simulates an endpoint that raises an unhandled generic exception.

        Raises:
            RuntimeError: Always raised to test unhandled server exception processing.
        """
        raise RuntimeError("unexpected error")

    return test_app


def test_database_operation_error_handler() -> None:
    """Tests that DatabaseOperationError is caught and yields a 500 status code with detail."""
    test_app = create_test_app()
    client = TestClient(test_app, raise_server_exceptions=False)

    response = client.get("/database-error")

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Database operation failed",
    }


def test_unexpected_error_handler() -> None:
    """Tests that unhandled generic exceptions return a 500 status code with a standard detail message."""
    test_app = create_test_app()
    client = TestClient(test_app, raise_server_exceptions=False)

    response = client.get("/unexpected-error")

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Internal server error",
    }