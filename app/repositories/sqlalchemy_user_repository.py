from sqlalchemy.orm import Session

from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository


class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy implementation of the UserRepository interface for user data operations.

    Attributes:
        _session (Session): The active SQLAlchemy database session used for transactions.
    """

    def __init__(self, session: Session) -> None:
        """Initializes the repository with a SQLAlchemy database session.

        Args:
            session (Session): The database session instance to be used by the repository.
        """
        self._session = session

    def create(self, user: UserModel) -> UserModel:
        """Persists a new user entity in the database.

        Args:
            user (UserModel): The user model instance to be created.

        Returns:
            UserModel: The newly created user model instance with updated database state.
        """
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    def list(self) -> list[UserModel]:
        """Retrieves all user entities from the database.

        Returns:
            list[UserModel]: A list containing all retrieved user model instances.
        """
        return self._session.query(UserModel).all()

    def find_by_id(self, user_id: int) -> UserModel | None:
        """Finds a user entity by its unique identifier.

        Args:
            user_id (int): The unique identifier of the user to search for.

        Returns:
            UserModel | None: The matching user model instance if found, or None.
        """
        return (
            self._session.query(UserModel)
            .filter(UserModel.id == user_id)
            .first()
        )

    def find_by_email(self, email: str) -> UserModel | None:
        """Finds a user entity by its unique email address.

        Args:
            email (str): The email address of the user to search for.

        Returns:
            UserModel | None: The matching user model instance if found, or None.
        """
        return (
            self._session.query(UserModel)
            .filter(UserModel.email == email)
            .first()
        )

    def update(self, user: UserModel) -> UserModel:
        """Updates an existing user entity in the database.

        Args:
            user (UserModel): The user model instance with updated attributes.

        Returns:
            UserModel: The refreshed user model instance reflecting updated database state.
        """
        self._session.commit()
        self._session.refresh(user)
        return user

    def delete(self, user: UserModel) -> None:
        """Deletes a user entity from the database.

        Args:
            user (UserModel): The user model instance to be removed.
        """
        self._session.delete(user)
        self._session.commit()