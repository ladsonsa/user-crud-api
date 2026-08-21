from collections.abc import Generator

from sqlalchemy.orm import Session, sessionmaker

from app.database.connection import engine

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db_session() -> Generator[Session, None, None]:
    """Provides a transactional database session for context management.

    Yields:
        Generator[Session, None, None]: A SQLAlchemy Session object.

    Yields:
        Session: An active database session instance.
    """
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()