import pytest

from app.dtos.user_update import UserUpdateDTO
from app.exceptions.user_exceptions import (
    DuplicateUserEmailError,
    UserNotFoundError,
)
from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository
from app.workflows.update_user import UpdateUserWorkflow


class FakeUserRepository(UserRepository):
    """In-memory mock repository implementation for testing user update operations.

    Attributes:
        users (list[UserModel]): Internal list storing persisted user instances.
    """

    def __init__(self) -> None:
        """Initializes the fake repository with an empty user collection."""
        self.users: list[UserModel] = []

    def create(self, user: UserModel) -> UserModel:
        """Simulates user creation by appending to the list.

        Args:
            user (UserModel): The user entity instance to store.

        Returns:
            UserModel: The stored user entity.
        """
        self.users.append(user)
        return user

    def list(self) -> list[UserModel]:
        """Retrieves all stored users.

        Returns:
            list[UserModel]: A list of all stored user entities.
        """
        return self.users

    def find_by_id(self, user_id: int) -> UserModel | None:
        """Finds a user by their unique identifier.

        Args:
            user_id (int): The unique identifier of the user to search for.

        Returns:
            UserModel | None: The matching user entity if found, None otherwise.
        """
        return next((user for user in self.users if user.id == user_id), None)

    def find_by_email(self, email: str) -> UserModel | None:
        """Finds a user by their email address.

        Args:
            email (str): The email address to search for.

        Returns:
            UserModel | None: The matching user entity if found, None otherwise.
        """
        return next((user for user in self.users if user.email == email), None)

    def update(self, user: UserModel) -> UserModel:
        """Simulates updating an existing user record.

        Args:
            user (UserModel): The user entity instance containing updated data.

        Returns:
            UserModel: The updated user entity instance.
        """
        return user

    def delete(self, user: UserModel) -> None:
        """Removes a user entity from the internal storage list.

        Args:
            user (UserModel): The user entity instance to remove.
        """
        self.users.remove(user)


def test_update_user_success() -> None:
    """Tests successful user update workflow execution with valid input data."""
    repository = FakeUserRepository()

    user = UserModel(name="Alice", email="alice@example.com")
    user.id = 1
    repository.users.append(user)

    workflow = UpdateUserWorkflow(repository)

    result = workflow.execute(
        1,
        UserUpdateDTO(name="Alice Smith", email="alice.smith@example.com"),
    )

    assert result.name == "Alice Smith"
    assert result.email == "alice.smith@example.com"


def test_update_user_not_found() -> None:
    """Tests that UpdateUserWorkflow raises UserNotFoundError when target user does not exist.

    Raises:
        UserNotFoundError: Expected exception when attempting to update a missing user.
    """
    workflow = UpdateUserWorkflow(FakeUserRepository())

    with pytest.raises(UserNotFoundError):
        workflow.execute(
        999,
        UserUpdateDTO(
            name="Test",
            email="test@example.com",
        ),
    )


def test_update_user_duplicate_email() -> None:
    """Tests that UpdateUserWorkflow raises DuplicateUserEmailError when new email is used by another user.

    Raises:
        DuplicateUserEmailError: Expected exception when updated email collides with existing user.
    """
    repository = FakeUserRepository()

    first = UserModel(name="Alice", email="alice@example.com")
    first.id = 1

    second = UserModel(name="Bob", email="bob@example.com")
    second.id = 2

    repository.users.extend([first, second])

    workflow = UpdateUserWorkflow(repository)

    with pytest.raises(DuplicateUserEmailError):
            workflow.execute(
        2,
        UserUpdateDTO(
            name="Bob",
            email="alice@example.com",
        ),
    )
