from collections.abc import Generator

from sqlalchemy.orm import Session, sessionmaker

from app.database.connection import engine

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db_session() -> Generator[Session]:
    """Provides a transactional database session for context management.

    Yields:
        Session: An active database session instance managed during the request lifecycle.
    """
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
