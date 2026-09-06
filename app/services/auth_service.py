from app.dtos.login import LoginDTO
from app.models.user_model import UserModel
from app.workflows.authenticate_user import AuthenticateUserWorkflow


class AuthService:
    """Service layer delegating authentication workflows and credentials management.

    Attributes:
        _authenticate_workflow (AuthenticateUserWorkflow): The workflow executing authentication logic.
    """

    def __init__(self, authenticate_workflow: AuthenticateUserWorkflow) -> None:
        """Initializes the service with the authentication workflow dependency.

        Args:
            authenticate_workflow (AuthenticateUserWorkflow): The workflow instance for authentication.
        """
        self._authenticate_workflow = authenticate_workflow

    def authenticate_user(self, data: LoginDTO) -> UserModel:
        """Authenticates a user using provided login credentials.

        Args:
            data (LoginDTO): The data transfer object containing user credentials.

        Returns:
            UserModel: The authenticated user entity instance.

        Raises:
            UserNotFoundError: If credentials verification fails.
        """
        return self._authenticate_workflow.execute(data)
