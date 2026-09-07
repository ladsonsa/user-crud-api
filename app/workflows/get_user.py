from app.exceptions.user_exceptions import (
    UserNotFoundError,
    UserOwnershipError,
)
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

    def execute(self, user_id: int, current_user: UserModel) -> UserModel:
        """Retrieves a user by ID and verifies that the current user owns the resource.

        Args:
            user_id (int): The unique identifier of the target user to retrieve.
            current_user (UserModel): The currently authenticated user requesting access.

        Returns:
            UserModel: The retrieved user entity instance.

        Raises:
            UserNotFoundError: If no user matching `user_id` exists in the repository.
            UserOwnershipError: If `current_user` does not have ownership of the target resource.
        """
        user = self._repository.find_by_id(user_id)

        if user is None:
            raise UserNotFoundError()

        if current_user.id != user.id:
            raise UserOwnershipError()

        return user
