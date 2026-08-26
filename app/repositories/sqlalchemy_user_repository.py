from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.exceptions.user_exceptions import (
    DatabaseOperationError,
    DuplicateUserEmailError,
)
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
        """Persists a new user record in the database.

        Args:
            user (UserModel): The user entity instance to be created.

        Returns:
            UserModel: The refreshed user entity instance after successful persistence.

        Raises:
            DuplicateUserEmailError: If the email uniqueness constraint is violated.
            DatabaseOperationError: If a general database failure occurs during execution.
        """
        try:
            self._session.add(user)
            self._session.commit()
            self._session.refresh(user)

            return user
        except IntegrityError as exc:
            self._session.rollback()
            raise DuplicateUserEmailError from exc
        except SQLAlchemyError as exc:
            self._session.rollback()
            raise DatabaseOperationError from exc

    def list(self) -> list[UserModel]:
        """Retrieves all user records from the database.

        Returns:
            list[UserModel]: A list of all persisted user model instances.
        """
        return self._session.query(UserModel).all()

    def find_by_id(self, user_id: int) -> UserModel | None:
        """Finds a user record by its unique identifier.

        Args:
            user_id (int): The unique identifier of the user to search for.

        Returns:
            UserModel | None: The matching user model instance if found, None otherwise.
        """
        return self._session.query(UserModel).filter(UserModel.id == user_id).first()

    def find_by_email(self, email: str) -> UserModel | None:
        """Finds a user record by its unique email address.

        Args:
            email (str): The email address of the user to search for.

        Returns:
            UserModel | None: The matching user model instance if found, None otherwise.
        """
        return self._session.query(UserModel).filter(UserModel.email == email).first()

    def update(self, user: UserModel) -> UserModel:
        """Persists updates to an existing user record in the database.

        Args:
            user (UserModel): The modified user entity instance to be updated.

        Returns:
            UserModel: The refreshed user entity instance after committing changes.

        Raises:
            DuplicateUserEmailError: If updating the user violates unique email constraints.
            DatabaseOperationError: If a general database failure occurs during execution.
        """
        try:
            self._session.commit()
            self._session.refresh(user)

            return user
        except IntegrityError as exc:
            self._session.rollback()
            raise DuplicateUserEmailError from exc

        except SQLAlchemyError as exc:
            self._session.rollback()
            raise DatabaseOperationError from exc

    def delete(self, user: UserModel) -> None:
        """Removes a user record from the database.

        Args:
            user (UserModel): The user entity instance to be deleted.

        Raises:
            DuplicateUserEmailError: If deletion violates database integrity constraints.
            DatabaseOperationError: If a general database failure occurs during execution.
        """
        try:
            self._session.delete(user)
            self._session.commit()
        except IntegrityError as exc:
            self._session.rollback()
            raise DuplicateUserEmailError from exc

        except SQLAlchemyError as exc:
            self._session.rollback()
            raise DatabaseOperationError from exc
