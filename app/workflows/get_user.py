from app.exceptions.user_exceptions import UserNotFoundError
from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository


class GetUserWorkflow:
    """Workflow component that handles the business logic for retrieving a specific user.

    Attributes:
        _repository (UserRepository): Repository instance used for user data persistence operations.
    """

    def __init__(self, repository: UserRepository) -> None:
        """Initializes the workflow with a user repository instance.

        Args:
            repository (UserRepository): The repository implementation to use for user data persistence.
        """
        self._repository = repository

    def execute(self, user_id: int) -> UserModel:
        """Executes the workflow to find and return a user by their unique identifier.

        Args:
            user_id (int): The unique identifier of the user to retrieve.

        Returns:
            UserModel: The matching user model instance.

        Raises:
            UserNotFoundError: If no user with the specified identifier is found.
        """
        user = self._repository.find_by_id(user_id)

        if user is None:
            raise UserNotFoundError()

        return user
