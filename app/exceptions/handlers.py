from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.user_exceptions import (
    DatabaseOperationError,
    DuplicateUserEmailError,
    UserNotFoundError,
)
from app.logs.logger import get_logger

logger = get_logger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """Registers custom exception handlers on the provided FastAPI application instance.

    Maps domain-specific exceptions to structured HTTP JSON responses.

    Args:
        app (FastAPI): The target FastAPI application instance.
    """

    @app.exception_handler(UserNotFoundError)
    async def user_not_found_handler(
        request: Request,
        exc: UserNotFoundError,
    ) -> JSONResponse:
        """Handles UserNotFoundError exceptions by returning a 404 Not Found response."""
        logger.warning("User not found")
        return JSONResponse(
            status_code=404,
            content={"detail": "User not found"},
        )

    @app.exception_handler(DuplicateUserEmailError)
    async def duplicate_email_handler(
        request: Request,
        exc: DuplicateUserEmailError,
    ) -> JSONResponse:
        """Handles DuplicateUserEmailError exceptions by returning a 409 Conflict response."""
        logger.warning("Duplicate email")
        return JSONResponse(
            status_code=409,
            content={"detail": "Email already exists"},
        )

    @app.exception_handler(DatabaseOperationError)
    async def database_error_handler(
        request: Request,
        exc: DatabaseOperationError,
    ) -> JSONResponse:
        """Handles DatabaseOperationError exceptions by returning a 500 Internal Server Error response."""
        logger.error("Database operation failed")
        return JSONResponse(
            status_code=500,
            content={"detail": "Database operation failed"},
        )

    @app.exception_handler(Exception)
    async def unexpected_error_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """Catch-all handler for unhandled exceptions, returning a generic 500 Internal Server Error response."""
        logger.exception("Unexpected application error")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )
