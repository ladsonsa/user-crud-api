from app.dtos.login import LoginDTO
from app.dtos.token_response import TokenResponseDTO
from app.services.auth_service import AuthService


class AuthController:
    """Controller component responsible for handling authentication-related HTTP requests and responses.

    Attributes:
        _service (AuthService): Service instance providing core authentication business logic.
    """

    def __init__(self, service: AuthService) -> None:
        """Initializes the authentication controller with an auth service instance.

        Args:
            service (AuthService): The service layer dependency for authentication operations.
        """
        self._service = service

    def authenticate_user(self, data: LoginDTO) -> TokenResponseDTO:
        """Handles the HTTP request to authenticate a user and issue access tokens.

        Args:
            data (LoginDTO): Data transfer object containing the user's login credentials.

        Returns:
            TokenResponseDTO: Response DTO containing the issued access token and type.
        """
        return self._service.authenticate_user(data)
