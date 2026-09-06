from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database.session import get_db_session
from app.exceptions.user_exceptions import AuthenticationError
from app.models.user_model import UserModel
from app.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.security.token import decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
    session: Annotated[Session, Depends(get_db_session)],
) -> UserModel:
    """Dependency provider that decodes the Bearer token and retrieves the current authenticated user.

    Setting `auto_error=False` on `HTTPBearer` allows missing or malformed header errors to be caught
    and unified into the domain-level `AuthenticationError`, ensuring consistent error handling
    and preventing credential or scheme leaks.

    Args:
        credentials (HTTPAuthorizationCredentials | None): The HTTP Bearer authorization credentials, if present.
        session (Session): The active SQLAlchemy database session injected by FastAPI.

    Returns:
        UserModel: The authenticated user entity instance.

    Raises:
        AuthenticationError: If the Bearer header is missing, token decoding fails, claims are invalid,
            or the referenced user does not exist in the database.
    """
    if credentials is None:
        raise AuthenticationError()

    try:
        payload = decode_access_token(credentials.credentials)
    except jwt.PyJWTError as exc:
        raise AuthenticationError() from exc

    subject = payload.get("sub")

    if not isinstance(subject, str):
        raise AuthenticationError()

    try:
        user_id = int(subject)
    except ValueError as exc:
        raise AuthenticationError() from exc

    repository = SQLAlchemyUserRepository(session)
    user = repository.find_by_id(user_id)

    if user is None:
        raise AuthenticationError()

    return user
