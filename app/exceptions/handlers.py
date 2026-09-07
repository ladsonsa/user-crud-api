from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions.user_exceptions import (
    AuthenticationError,
    DatabaseOperationError,
    DuplicateUserEmailError,
    UserNotFoundError,
    UserOwnershipError,
)
from app.logs.logger import get_logger

logger = get_logger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """Registers custom exception handlers on the provided FastAPI application instance.

    Maps domain-specific exceptions to structured HTTP JSON responses.

    Args:
        app (FastAPI): The target FastAPI application instance.
    """

    @app.exception_handler(AuthenticationError)
    async def authentication_error_handler(
        request: Request,
        exc: AuthenticationError,
    ) -> JSONResponse:
        """Global exception handler for domain-level `AuthenticationError`.

        Catches all authentication failures across the application lifecycle and standardizes
        them into an HTTP 401 Unauthorized response with the required `WWW-Authenticate` header.
        Logs warnings without exposing sensitive security credentials or details to the client.

        Args:
            request (Request): The incoming HTTP request instance that triggered the exception.
            exc (AuthenticationError): The caught authentication exception instance.

        Returns:
            JSONResponse: A 401 Unauthorized JSON response with standard error details.
        """
        logger.warning(
            "Authentication failed for request %s %s: %s",
            request.method,
            request.url.path,
            exc,
        )
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
            content={"detail": "Invalid authentication credentials"},
        )

    @app.exception_handler(UserNotFoundError)
    async def user_not_found_handler(
        request: Request,
        exc: UserNotFoundError,
    ) -> JSONResponse:
        """Handles UserNotFoundError exceptions by returning a 404 Not Found response.

        Args:
            request (Request): The incoming HTTP request instance that triggered the exception.
            exc (UserNotFoundError): The caught user not found exception instance.

        Returns:
            JSONResponse: A 404 Not Found JSON response with error details.
        """
        logger.warning(
            "User resource not found for request %s %s",
            request.method,
            request.url.path,
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "User not found"},
        )

    @app.exception_handler(UserOwnershipError)
    async def user_ownership_error_handler(
        request: Request,
        exc: UserOwnershipError,
    ) -> JSONResponse:
        """Handles UserOwnershipError exceptions by returning a 403 Forbidden response.

        Args:
            request (Request): The incoming HTTP request instance that triggered the exception.
            exc (UserOwnershipError): The caught user ownership exception instance.

        Returns:
            JSONResponse: A 403 Forbidden JSON response indicating insufficient permissions.
        """
        logger.warning(
            "Unauthorized user resource access attempted on %s %s",
            request.method,
            request.url.path,
        )

        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "You do not have permission to access this user."},
        )

    @app.exception_handler(DuplicateUserEmailError)
    async def duplicate_email_handler(
        request: Request,
        exc: DuplicateUserEmailError,
    ) -> JSONResponse:
        """Handles DuplicateUserEmailError exceptions by returning a 409 Conflict response.

        Args:
            request (Request): The incoming HTTP request instance that triggered the exception.
            exc (DuplicateUserEmailError): The caught duplicate email exception instance.

        Returns:
            JSONResponse: A 409 Conflict JSON response indicating the email is already in use.
        """
        logger.warning(
            "Duplicate user email registration attempted on %s %s",
            request.method,
            request.url.path,
        )
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Email already exists"},
        )

    @app.exception_handler(DatabaseOperationError)
    async def database_error_handler(
        request: Request,
        exc: DatabaseOperationError,
    ) -> JSONResponse:
        """Handles DatabaseOperationError exceptions by returning a 500 Internal Server Error response.

        Args:
            request (Request): The incoming HTTP request instance that triggered the exception.
            exc (DatabaseOperationError): The caught database operation exception instance.

        Returns:
            JSONResponse: A 500 Internal Server Error JSON response indicating a persistence failure.
        """
        logger.error(
            "Database operation error during %s %s: %s",
            request.method,
            request.url.path,
            exc,
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Database operation failed"},
        )

    @app.exception_handler(Exception)
    async def unexpected_error_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """Catch-all handler for unhandled exceptions, returning a generic 500 Internal Server Error response.

        Args:
            request (Request): The incoming HTTP request instance that triggered the exception.
            exc (Exception): The unhandled exception instance caught at runtime.

        Returns:
            JSONResponse: A generic 500 Internal Server Error JSON response.
        """
        logger.exception(
            "Unhandled exception caught on %s %s: %s",
            request.method,
            request.url.path,
            exc,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )
