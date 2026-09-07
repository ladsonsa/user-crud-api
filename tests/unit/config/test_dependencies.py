from unittest.mock import MagicMock, patch

from app.config.dependencies import get_auth_controller
from app.controllers.auth_controller import AuthController


@patch("app.config.dependencies.AuthService")
@patch("app.config.dependencies.AuthenticateUserWorkflow")
@patch("app.config.dependencies.SQLAlchemyUserRepository")
def test_get_auth_controller(
    mock_repository: MagicMock,
    mock_workflow: MagicMock,
    mock_service: MagicMock,
) -> None:
    """Tests that get_auth_controller correctly wires dependencies and returns an AuthController instance.

    Verifies the instantiation chain: SQLAlchemyUserRepository -> AuthenticateUserWorkflow -> AuthService -> AuthController.

    Args:
        mock_repository (MagicMock): Mock for the repository factory.
        mock_workflow (MagicMock): Mock for the authentication workflow factory.
        mock_service (MagicMock): Mock for the authentication service factory.
    """
    session = MagicMock()

    result = get_auth_controller(session)

    mock_repository.assert_called_once_with(session)
    mock_workflow.assert_called_once_with(mock_repository.return_value)
    mock_service.assert_called_once_with(
        authenticate_workflow=mock_workflow.return_value,
    )
    assert isinstance(result, AuthController)
