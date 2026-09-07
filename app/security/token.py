from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from app.config.settings import get_settings


def create_access_token(subject: str) -> str:
    """Generates a signed JWT access token for a given subject.

    Calculates the expiration time based on application settings and encodes
    the payload using the configured secret key and algorithm.

    Args:
        subject (str): The entity identifier (e.g., user ID or email) stored in the 'sub' claim.

    Returns:
        str: The encoded JSON Web Token string.
    """
    settings = get_settings()
    expires_at = datetime.now(UTC) + timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": subject,
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    """Decodes and validates a JSON Web Token string.

    Verifies the signature and expiration claims against application settings.

    Args:
        token (str): The JWT string to decode and validate.

    Returns:
        dict[str, Any]: The decoded JWT payload dictionary containing claims.

    Raises:
        jwt.PyJWTError: If the token signature is invalid or expired.
    """
    settings = get_settings()

    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )
