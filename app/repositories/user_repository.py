from abc import ABC, abstractmethod

from app.models.user_model import UserModel


class UserRepository(ABC):
    """Abstract interface defining the repository contract for user data persistence."""

    @abstractmethod
    def create(self, user: UserModel) -> UserModel:
        """Persists a new user entity in the repository.

        Args:
            user (UserModel): The user model instance to be created.

        Returns:
            UserModel: The newly created user model instance with generated fields.

        Raises:
            NotImplementedError: Raised when the abstract method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[UserModel]:
        """Retrieves all user entities stored in the repository.

        Returns:
            list[UserModel]: A list containing all retrieved user model instances.

        Raises:
            NotImplementedError: Raised when the abstract method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, user_id: int) -> UserModel | None:
        """Finds a user entity by its unique identifier.

        Args:
            user_id (int): The unique identifier of the user to search for.

        Returns:
            UserModel | None: The matching user model instance if found, or None.

        Raises:
            NotImplementedError: Raised when the abstract method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_email(self, email: str) -> UserModel | None:
        """Finds a user entity by its unique email address.

        Args:
            email (str): The email address of the user to search for.

        Returns:
            UserModel | None: The matching user model instance if found, or None.

        Raises:
            NotImplementedError: Raised when the abstract method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, user: UserModel) -> UserModel:
        """Updates an existing user entity in the repository.

        Args:
            user (UserModel): The user model instance with updated attributes.

        Returns:
            UserModel: The updated user model instance.

        Raises:
            NotImplementedError: Raised when the abstract method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, user: UserModel) -> None:
        """Deletes a user entity from the repository.

        Args:
            user (UserModel): The user model instance to be removed.

        Raises:
            NotImplementedError: Raised when the abstract method is not implemented.
        """
        raise NotImplementedError
