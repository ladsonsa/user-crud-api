from app.dtos.login import LoginDTO
from app.dtos.token_response import TokenResponseDTO
from app.security.token import create_access_token
from app.workflows.authenticate_user import AuthenticateUserWorkflow


class AuthService:
    """Service layer handling user authentication and security token issuance.

    Attributes:
        _authenticate_workflow (AuthenticateUserWorkflow): Workflow verifying credentials.
    """

    def __init__(self, authenticate_workflow: AuthenticateUserWorkflow) -> None:
        """Initializes the authentication service with required workflows.

        Args:
            authenticate_workflow (AuthenticateUserWorkflow): Workflow instance for credentials validation.
        """
        self._authenticate_workflow = authenticate_workflow

    def authenticate_user(self, data: LoginDTO) -> TokenResponseDTO:
        """Authenticates user credentials and generates a bearer access token response.

        Args:
            data (LoginDTO): Data transfer object containing user login credentials.

        Returns:
            TokenResponseDTO: Data transfer object containing the generated JWT access token and token type.
        """
        user = self._authenticate_workflow.execute(data)
        access_token = create_access_token(str(user.id))

        return TokenResponseDTO(
            access_token=access_token,
            token_type="bearer",
        )
