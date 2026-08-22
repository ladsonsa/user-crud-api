import pytest

from app.dtos.user_create import UserCreateDTO
from app.exceptions.user_exceptions import DuplicateUserEmailError
from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository
from app.workflows.create_user import CreateUserWorkflow


class FakeUserRepository(UserRepository):
    """In-memory mock repository implementation for testing user operations.

    Attributes:
        users (list[UserModel]): Internal list storing persisted user instances.
    """

    def __init__(self) -> None:
        """Initializes the fake repository with an empty user collection."""
        self.users: list[UserModel] = []

    def create(self, user: UserModel) -> UserModel:
        """Simulates user creation by assigning an ID and appending to the list.

        Args:
            user (UserModel): The user entity instance to store.

        Returns:
            UserModel: The stored user entity with an assigned ID.
        """
        user.id = len(self.users) + 1
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


def test_create_user_success() -> None:
    """Tests successful user creation workflow execution with valid input data."""
    repository = FakeUserRepository()
    workflow = CreateUserWorkflow(repository)

    data = UserCreateDTO(
        name="Alice",
        email="alice@example.com",
    )

    user = workflow.execute(data)

    assert user.id == 1
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    assert len(repository.users) == 1

def test_create_user_duplicate_email() -> None:
    """Tests that the user creation workflow raises DuplicateUserEmailError when given an existing email.

    Raises:
        DuplicateUserEmailError: Expected exception when attempting to create a user with a duplicate email.
    """
    repository = FakeUserRepository()
    workflow = CreateUserWorkflow(repository)

    existing_user = UserModel(
        name="Alice",
        email="alice@example.com",
    )
    existing_user.id = 1
    repository.users.append(existing_user)

    data = UserCreateDTO(
        name="Bob",
        email="alice@example.com",
    )

    with pytest.raises(DuplicateUserEmailError):
        workflow.execute(data)

    assert len(repository.users) == 1