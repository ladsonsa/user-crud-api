from app.database.init_db import init_database
from app.database.session import SessionLocal
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