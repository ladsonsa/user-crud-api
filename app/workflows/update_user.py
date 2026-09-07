from app.dtos.user_update import UserUpdateDTO
from app.exceptions.user_exceptions import (
    DuplicateUserEmailError,
    UserNotFoundError,
    UserOwnershipError,
)
from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository


class UpdateUserWorkflow:
    """Workflow handling user attribute updates after ownership and email conflict validations.

    Attributes:
        _repository (UserRepository): Repository interface for user data access operations.
    """

    def __init__(self, repository: UserRepository) -> None:
        """Initializes the workflow with a user repository instance.

        Args:
            repository (UserRepository): The user repository implementation to use.
        """
        self._repository = repository

    def execute(
        self,
        user_id: int,
        data: UserUpdateDTO,
        current_user: UserModel,
    ) -> UserModel:
        """Updates user details for a specified user ID after validating existence, ownership, and unique email constraints.

        Args:
            user_id (int): The unique identifier of the user to update.
            data (UserUpdateDTO): Data transfer object containing the fields to update.
            current_user (UserModel): The currently authenticated user requesting the update.

        Returns:
            UserModel: The updated user entity instance.

        Raises:
            UserNotFoundError: If no user matching `user_id` exists.
            UserOwnershipError: If `current_user` does not match the requested user ID.
            DuplicateUserEmailError: If the new email address is already registered to another user.
        """
        user = self._repository.find_by_id(user_id)

        if user is None:
            raise UserNotFoundError()

        if current_user.id != user.id:
            raise UserOwnershipError()

        if data.email is not None:
            existing_user = self._repository.find_by_email(data.email)

            if existing_user is not None and existing_user.id != user.id:
                raise DuplicateUserEmailError()

            user.email = data.email

        if data.name is not None:
            user.name = data.name

        return self._repository.update(user)
