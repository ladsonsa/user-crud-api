from app.database.connection import engine
from app.models.user_model import Base


def init_database() -> None:
    """Initializes the database schema by creating all defined tables.

    Executes DDL statements to create tables associated with the DeclarativeBase
    metadata if they do not already exist in the database.
    """
    Base.metadata.create_all(bind=engine)
