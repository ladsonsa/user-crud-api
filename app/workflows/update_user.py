from app.dtos.user_update import UserUpdateDTO
from app.exceptions.user_exceptions import DuplicateUserEmailError, UserNotFoundError
from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository


class UpdateUserWorkflow:
    """Workflow component that handles the business logic for updating an existing user.

    Attributes:
        _repository (UserRepository): Repository instance used for user data persistence operations.
    """

    def __init__(self, repository: UserRepository) -> None:
        """Initializes the workflow with a user repository instance.

        Args:
            repository (UserRepository): The repository implementation to use for user data persistence.
        """
        self._repository = repository

    def execute(self, user_id: int, data: UserUpdateDTO) -> UserModel:
        """Executes the user update workflow.

        Validates user existence and ensures email uniqueness before updating specified fields.

        Args:
            user_id (int): The unique identifier of the user to update.
            data (UserUpdateDTO): Data transfer object containing the fields to be updated.

        Returns:
            UserModel: The updated user model instance.

        Raises:
            UserNotFoundError: If no user with the specified identifier is found.
            DuplicateUserEmailError: If the new email belongs to another user.
        """
        user = self._repository.find_by_id(user_id)

        if user is None:
            raise UserNotFoundError()

        if data.email is not None:
            existing_user = self._repository.find_by_email(data.email)

            if existing_user is not None and existing_user.id != user.id:
                raise DuplicateUserEmailError()

            user.email = data.email

        if data.name is not None:
            user.name = data.name

        return self._repository.update(user)
