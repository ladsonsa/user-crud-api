from app.dtos.login import LoginDTO
from app.exceptions.user_exceptions import AuthenticationError
from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository
from app.security.password import verify_password


class AuthenticateUserWorkflow:
    """Workflow handling user authentication against stored credentials.

    Attributes:
        repository (UserRepository): Repository interface for user data access operations.
    """

    def __init__(self, repository: UserRepository) -> None:
        """Initializes the workflow with a user repository instance.

        Args:
            repository (UserRepository): The user repository implementation to use.
        """
        self.repository = repository

    def execute(self, data: LoginDTO) -> UserModel:
        """Validates user credentials and returns the authenticated user entity.

        Args:
            data (LoginDTO): Data transfer object containing login credentials.

        Returns:
            UserModel: The authenticated user entity instance.

        Raises:
            AuthenticationError: If no user matches the email or the password verification fails.
        """
        user = self.repository.find_by_email(data.email)

        if user is None:
            raise AuthenticationError

        if not verify_password(data.password, user.password_hash):
            raise AuthenticationError

        return user
