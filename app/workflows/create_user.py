from app.dtos.user_create import UserCreateDTO
from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository


class CreateUserWorkflow:
    """Workflow component that handles the business logic for creating a new user.

    Attributes:
        _repository (UserRepository): Repository instance used for user data persistence operations.
    """

    def __init__(self, repository: UserRepository) -> None:
        """Initializes the workflow with a user repository instance.

        Args:
            repository (UserRepository): The repository implementation to use for user data persistence.
        """
        self._repository = repository

    def execute(self, data: UserCreateDTO) -> UserModel:
        """Executes the user creation workflow.

        Validates whether the email is already registered before persisting the new user entity.

        Args:
            data (UserCreateDTO): Data transfer object containing the details for the new user.

        Returns:
            UserModel: The newly created and persisted user model instance.

        Raises:
            ValueError: If a user with the specified email already exists.
        """
        existing_user = self._repository.find_by_email(data.email)

        if existing_user is not None:
            raise ValueError("Email already exists")

        user = UserModel(
            name=data.name,
            email=data.email,
        )

        return self._repository.create(user)