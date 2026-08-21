from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


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
        """Build the SQLAlchemy database URL.

        Returns:
            str: PostgreSQL connection string.
        """

        return (
            f"postgresql+psycopg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/"
            f"{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance.

    Returns:
        Settings: Cached application settings.
    """

    return Settings()