from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.config.settings import get_settings


def create_engine_instance() -> Engine:
    """Creates and configures a new SQLAlchemy database engine instance.

    Retrieves database settings and initializes a database engine with connection
    health checking enabled via `pool_pre_ping`.

    Returns:
        Engine: A configured SQLAlchemy database engine instance.
    """
    settings = get_settings()

    return create_engine(
        settings.database_url,
        pool_pre_ping=True,
        future=True,
    )


engine = create_engine_instance()