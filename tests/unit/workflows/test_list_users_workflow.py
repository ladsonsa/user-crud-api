from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository
from app.workflows.list_users import ListUsersWorkflow


class FakeUserRepository(UserRepository):
    """In-memory mock repository implementation for testing user listing operations.

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


def test_list_users_returns_all_users() -> None:
    """Tests that ListUsersWorkflow retrieves all persisted user records from the repository."""
    repository = FakeUserRepository()

    first = UserModel(name="Alice", email="alice@example.com")
    first.id = 1

    second = UserModel(name="Bob", email="bob@example.com")
    second.id = 2

    repository.users.extend([first, second])

    workflow = ListUsersWorkflow(repository)

    result = workflow.execute()

    assert len(result) == 2
    assert result[0].name == "Alice"
    assert result[1].name == "Bob"
