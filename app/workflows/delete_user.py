from app.exceptions.user_exceptions import UserNotFoundError, UserOwnershipError
from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository


class DeleteUserWorkflow:
    """Workflow handling user account deletion after verifying existence and ownership.

    Attributes:
        _repository (UserRepository): Repository interface for user data access operations.
    """

    def __init__(self, repository: UserRepository) -> None:
        """Initializes the workflow with a user repository instance.

        Args:
            repository (UserRepository): The user repository implementation to use.
        """
        self._repository = repository

    def execute(self, user_id: int, current_user: UserModel) -> None:
        """Deletes a user account by ID after validating existence and ownership.

        Args:
            user_id (int): The unique identifier of the user to delete.
            current_user (UserModel): The currently authenticated user requesting deletion.

        Raises:
            UserNotFoundError: If no user matching `user_id` exists.
            UserOwnershipError: If `current_user` does not have ownership of the target resource.
        """
        user = self._repository.find_by_id(user_id)

        if user is None:
            raise UserNotFoundError()

        if current_user.id != user.id:
            raise UserOwnershipError()

        self._repository.delete(user)
