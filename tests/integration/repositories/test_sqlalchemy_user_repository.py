from unittest.mock import patch

import pytest
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.database.init_db import init_database
from app.database.session import SessionLocal
from app.exceptions.user_exceptions import (
    DatabaseOperationError,
    DuplicateUserEmailError,
)
from app.models.user_model import UserModel
from app.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository


def setup_module() -> None:
    """Prepares the test module environment by initializing the database schema."""
    init_database()


def test_repository_create_and_find_by_id() -> None:
    """Tests persisting a new user and retrieving it by unique identifier."""
    session = SessionLocal()

    try:
        repository = SQLAlchemyUserRepository(session)

        user = UserModel(
            name="Alice",
            email="alice.repository@example.com",
        )

        created = repository.create(user)
        found = repository.find_by_id(created.id)

        assert found is not None
        assert found.id == created.id
        assert found.name == "Alice"
    finally:
        session.close()


def test_repository_find_by_email() -> None:
    """Tests retrieving a persisted user record by email address."""
    session = SessionLocal()

    try:
        repository = SQLAlchemyUserRepository(session)

        user = UserModel(
            name="Bob",
            email="bob.repository@example.com",
        )

        repository.create(user)

        found = repository.find_by_email("bob.repository@example.com")

        assert found is not None
        assert found.email == "bob.repository@example.com"
    finally:
        session.close()


def test_repository_update() -> None:
    """Tests updating attributes of an existing user record in the repository."""
    session = SessionLocal()

    try:
        repository = SQLAlchemyUserRepository(session)

        user = UserModel(
            name="Carol",
            email="carol.repository@example.com",
        )

        created = repository.create(user)

        created.name = "Carol Updated"

        updated = repository.update(created)

        assert updated.name == "Carol Updated"
    finally:
        session.close()


def test_repository_delete() -> None:
    """Tests removing a user record from the database using the repository."""
    session = SessionLocal()

    try:
        repository = SQLAlchemyUserRepository(session)

        user = UserModel(
            name="Dave",
            email="dave.repository@example.com",
        )

        created = repository.create(user)

        repository.delete(created)

        assert repository.find_by_id(created.id) is None
    finally:
        session.close()


def test_repository_create_duplicate_email() -> None:
    """Tests that attempting to create a user with a duplicate email address raises DuplicateUserEmailError.

    Raises:
        DuplicateUserEmailError: Expected exception when attempting to insert a duplicate email.
    """
    session = SessionLocal()

    try:
        repository = SQLAlchemyUserRepository(session)

        first = UserModel(
            name="Duplicate First",
            email="duplicate.repository@example.com",
        )

        second = UserModel(
            name="Duplicate Second",
            email="duplicate.repository@example.com",
        )

        repository.create(first)

        with pytest.raises(DuplicateUserEmailError):
            repository.create(second)

        assert repository.find_by_email("duplicate.repository@example.com") is not None
    finally:
        session.close()


def test_repository_create_database_error_rolls_back() -> None:
    """Tests that an integrity error during user creation raises DuplicateUserEmailError and maintains session state.

    Raises:
        DuplicateUserEmailError: Expected exception when commit fails due to an integrity constraint.
    """
    session = SessionLocal()

    try:
        repository = SQLAlchemyUserRepository(session)

        user = UserModel(
            name="Rollback",
            email="rollback.repository@example.com",
        )

        with patch.object(
            session,
            "commit",
            side_effect=IntegrityError(
                "statement",
                {},
                Exception("database error"),
            ),
        ):
            with pytest.raises(DuplicateUserEmailError):
                repository.create(user)

        assert session.is_active
    finally:
        session.close()


def test_repository_create_database_error_rolls_back() -> None:
    """Tests that a database error during user creation triggers a transaction rollback and raises DatabaseOperationError.

    Raises:
        DatabaseOperationError: Expected exception when database user creation fails.
    """
    session = SessionLocal()

    try:
        repository = SQLAlchemyUserRepository(session)

        user = UserModel(
            name="Database Error",
            email="database-error.repository@example.com",
        )

        with patch.object(
            session,
            "commit",
            side_effect=SQLAlchemyError("database error"),
        ):
            with patch.object(
                session,
                "rollback",
                wraps=session.rollback,
            ) as rollback:
                with pytest.raises(DatabaseOperationError):
                    repository.create(user)

                rollback.assert_called_once()
    finally:
        session.close()


def test_repository_update_database_error_rolls_back() -> None:
    """Tests that a database error during user update triggers a transaction rollback and raises DatabaseOperationError.

    Raises:
        DatabaseOperationError: Expected exception when database user update fails.
    """
    session = SessionLocal()

    try:
        repository = SQLAlchemyUserRepository(session)

        user = UserModel(
            name="Update Error",
            email="update-error.repository@example.com",
        )

        created = repository.create(user)
        created.name = "Updated"

        with patch.object(
            session,
            "commit",
            side_effect=SQLAlchemyError("database error"),
        ):
            with patch.object(
                session,
                "rollback",
                wraps=session.rollback,
            ) as rollback:
                with pytest.raises(DatabaseOperationError):
                    repository.update(created)

                rollback.assert_called_once()
    finally:
        session.close()


def test_repository_delete_database_error_rolls_back() -> None:
    """Tests that a database error during user deletion triggers a transaction rollback and raises DatabaseOperationError.

    Raises:
        DatabaseOperationError: Expected exception when database user deletion fails.
    """
    session = SessionLocal()

    try:
        repository = SQLAlchemyUserRepository(session)

        user = UserModel(
            name="Delete Error",
            email="delete-error.repository@example.com",
        )

        created = repository.create(user)

        with patch.object(
            session,
            "commit",
            side_effect=SQLAlchemyError("database error"),
        ):
            with patch.object(
                session,
                "rollback",
                wraps=session.rollback,
            ) as rollback:
                with pytest.raises(DatabaseOperationError):
                    repository.delete(created)

                rollback.assert_called_once()

        session.expire_all()
        assert repository.find_by_id(created.id) is not None
    finally:
        session.close()
