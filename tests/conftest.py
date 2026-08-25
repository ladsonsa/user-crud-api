import pytest
from sqlalchemy import delete

from app.database.session import SessionLocal
from app.models.user_model import UserModel


@pytest.fixture(autouse=True)
def clean_database() -> None:
    """Fixture to automatically clear the UserModel table before each test run.

    Ensures test isolation by removing all existing user records from the database
    and committing the transaction before executing individual tests.
    """
    session = SessionLocal()
    session.execute(delete(UserModel))
    session.commit()
    session.close()
