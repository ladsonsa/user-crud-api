from app.config.settings import Settings


def test_database_url_handles_special_characters_in_password() -> None:
    """Tests that special characters in database passwords are URL-encoded in database_url.

    Verifies that characters like '@' and '/' are properly percent-encoded to prevent
    connection string parsing errors.
    """
    settings = Settings(
        postgres_db="testdb",
        postgres_user="testuser",
        postgres_password="p@ss/word",
        postgres_host="localhost",
        postgres_port=5432,
    )

    assert settings.database_url == (
        "postgresql+psycopg://testuser:p%40ss%2Fword@localhost:5432/testdb"
    )
