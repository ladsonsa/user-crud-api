from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository


class ListUsersWorkflow:
    """Workflow component that handles the business logic for retrieving all users.

    Attributes:
        _repository (UserRepository): Repository instance used for user data
        persistence operations.
    """

    def __init__(self, repository: UserRepository) -> None:
        """Initializes the workflow with a user repository instance.

        Args:
            repository (UserRepository): The repository implementation to use for user
            data persistence.
        """
        self._repository = repository

    def execute(self) -> list[UserModel]:
        """Executes the workflow to list all stored user entities.

        Returns:
            list[UserModel]: A list containing all retrieved user model instances.
        """
        return self._repository.list()
