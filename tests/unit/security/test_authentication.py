from unittest.mock import MagicMock, patch

import jwt
import pytest

from app.exceptions.user_exceptions import AuthenticationError
from app.models.user_model import UserModel
from app.security.authentication import get_current_user


def test_get_current_user_without_credentials() -> None:
    """Tests that get_current_user raises AuthenticationError when no credentials are provided."""
    with pytest.raises(AuthenticationError):
        get_current_user(None, MagicMock())


@patch("app.security.authentication.decode_access_token")
def test_get_current_user_with_invalid_token(
    mock_decode_access_token: MagicMock,
) -> None:
    """Tests that get_current_user raises AuthenticationError when token decoding fails."""
    mock_decode_access_token.side_effect = jwt.InvalidTokenError("Invalid token")

    credentials = MagicMock()
    credentials.credentials = "invalid-token"

    with pytest.raises(AuthenticationError):
        get_current_user(credentials, MagicMock())


@patch("app.security.authentication.decode_access_token")
def test_get_current_user_without_valid_subject(
    mock_decode_access_token: MagicMock,
) -> None:
    """Tests that get_current_user raises AuthenticationError when decoded token lacks a subject claim."""
    mock_decode_access_token.return_value = {}

    credentials = MagicMock()
    credentials.credentials = "valid-token"

    with pytest.raises(AuthenticationError):
        get_current_user(credentials, MagicMock())


@patch("app.security.authentication.SQLAlchemyUserRepository")
@patch("app.security.authentication.decode_access_token")
def test_get_current_user_with_nonexistent_user(
    mock_decode_access_token: MagicMock,
    mock_repository: MagicMock,
) -> None:
    """Tests that get_current_user raises AuthenticationError when token subject does not match any user."""
    mock_decode_access_token.return_value = {"sub": "999999"}
    mock_repository.return_value.find_by_id.return_value = None

    credentials = MagicMock()
    credentials.credentials = "valid-token"

    with pytest.raises(AuthenticationError):
        get_current_user(credentials, MagicMock())


@patch("app.security.authentication.SQLAlchemyUserRepository")
@patch("app.security.authentication.decode_access_token")
def test_get_current_user_success(
    mock_decode_access_token: MagicMock,
    mock_repository: MagicMock,
) -> None:
    """Tests successful authentication and retrieval of the current user instance."""
    user = UserModel(
        id=1,
        name="Test User",
        email="test@example.com",
        password_hash="hashed-password",
    )

    mock_decode_access_token.return_value = {"sub": "1"}
    mock_repository.return_value.find_by_id.return_value = user

    credentials = MagicMock()
    credentials.credentials = "valid-token"

    result = get_current_user(credentials, MagicMock())

    assert result is user


@patch("app.security.authentication.decode_access_token")
def test_get_current_user_with_expired_token(
    mock_decode_access_token: MagicMock,
) -> None:
    """Tests that resolving the current user with an expired JWT token raises an AuthenticationError.

    Args:
        mock_decode_access_token (MagicMock): Mock function for token decoding patched to raise ExpiredSignatureError.
    """
    mock_decode_access_token.side_effect = jwt.ExpiredSignatureError(
        "Signature has expired"
    )

    credentials = MagicMock()
    credentials.credentials = "expired-token"

    with pytest.raises(AuthenticationError):
        get_current_user(credentials, MagicMock())
