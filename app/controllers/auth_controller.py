from app.dtos.login import LoginDTO
from app.models.user_model import UserModel
from app.services.auth_service import AuthService


class AuthController:
    """Controller handling HTTP-level orchestration for authentication endpoints.

    Attributes:
        _service (AuthService): The authentication domain service instance.
    """

    def __init__(self, service: AuthService) -> None:
        """Initializes the controller with the authentication service dependency.

        Args:
            service (AuthService): The authentication domain service instance.
        """
        self._service = service

    def authenticate_user(self, data: LoginDTO) -> UserModel:
        """Orchestrates authentication request data processing and delegates to the service layer.

        Args:
            data (LoginDTO): The validated login data transfer object.

        Returns:
            UserModel: The authenticated user entity instance.

        Raises:
            UserNotFoundError: If authentication credentials are invalid or user is not found.
        """
        return self._service.authenticate_user(data)
