from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    """Store application and database configuration loaded from environment variables.

    Attributes:
        app_name: Application name.
        app_env: Application environment.
        app_host: Host used by the HTTP server.
        app_port: Port used by the HTTP server.
        postgres_db: PostgreSQL database name.
        postgres_user: PostgreSQL username.
        postgres_password: PostgreSQL password.
        postgres_host: PostgreSQL host.
        postgres_port: PostgreSQL port.
    """

    app_name: str = "user-crud-api"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def database_url(self) -> str:
        """Constructs and returns the full PostgreSQL database connection URL.

        Uses SQLAlchemy's URL builder to assemble credentials and server details into a
        properly escaped connection string using the psycopg driver.

        Returns:
            str: The complete rendered database URL string.
        """
        return URL.create(
            "postgresql+psycopg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        ).render_as_string(hide_password=False)


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance.

    Returns:
        Settings: Cached application settings.
    """

    return Settings()
