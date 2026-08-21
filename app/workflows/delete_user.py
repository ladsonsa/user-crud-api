from app.repositories.user_repository import UserRepository


class DeleteUserWorkflow:
    """Workflow component that handles the business logic for deleting a user.

    Attributes:
        _repository (UserRepository): Repository instance used for user data persistence operations.
    """

    def __init__(self, repository: UserRepository) -> None:
        """Initializes the workflow with a user repository instance.

        Args:
            repository (UserRepository): The repository implementation to use for user data persistence.
        """
        self._repository = repository

    def execute(self, user_id: int) -> None:
        """Executes the workflow to delete a user by their unique identifier.

        Args:
            user_id (int): The unique identifier of the user to delete.

        Raises:
            ValueError: If no user with the specified identifier is found.
        """
        user = self._repository.find_by_id(user_id)

        if user is None:
            raise ValueError("User not found")

        self._repository.delete(user)
