from unittest.mock import MagicMock, patch

import pytest

from app.dtos.login import LoginDTO
from app.exceptions.user_exceptions import AuthenticationError
from app.models.user_model import UserModel
from app.workflows.authenticate_user import AuthenticateUserWorkflow


@pytest.fixture
def repository() -> MagicMock:
    return MagicMock()


@pytest.fixture
def workflow(repository: MagicMock) -> AuthenticateUserWorkflow:
    return AuthenticateUserWorkflow(repository)


@pytest.fixture
def login_data() -> LoginDTO:
    return LoginDTO(
        email="user@example.com",
        password="SecurePassword123",
    )


@pytest.fixture
def user() -> UserModel:
    return UserModel(
        id=1,
        name="Test User",
        email="user@example.com",
        password_hash="hashed-password",
    )


def test_authenticate_user_success(
    workflow: AuthenticateUserWorkflow,
    repository: MagicMock,
    login_data: LoginDTO,
    user: UserModel,
) -> None:
    """Tests successful authentication with matching email and valid password."""
    repository.find_by_email.return_value = user

    with patch(
        "app.workflows.authenticate_user.verify_password",
        return_value=True,
    ):
        result = workflow.execute(login_data)

    assert result is user
    repository.find_by_email.assert_called_once_with(login_data.email)


def test_authenticate_user_not_found(
    workflow: AuthenticateUserWorkflow,
    repository: MagicMock,
    login_data: LoginDTO,
) -> None:
    """Tests that authentication fails with AuthenticationError when the user email does not exist."""
    repository.find_by_email.return_value = None

    with pytest.raises(AuthenticationError):
        workflow.execute(login_data)

    repository.find_by_email.assert_called_once_with(login_data.email)


def test_authenticate_user_invalid_password(
    workflow: AuthenticateUserWorkflow,
    repository: MagicMock,
    login_data: LoginDTO,
    user: UserModel,
) -> None:
    """Tests that authentication fails with AuthenticationError when an incorrect password is provided."""
    repository.find_by_email.return_value = user

    with patch(
        "app.workflows.authenticate_user.verify_password",
        return_value=False,
    ):
        with pytest.raises(AuthenticationError):
            workflow.execute(login_data)

    repository.find_by_email.assert_called_once_with(login_data.email)
