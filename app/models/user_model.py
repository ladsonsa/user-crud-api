from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base declarative class for SQLAlchemy models."""

    pass


class UserModel(Base):
    """Database model representing a user entity in the application.

    Attributes:
        id (Mapped[int]): Primary key identifier for the user.
        name (Mapped[str]): Full name of the user, up to 100 characters.
        email (Mapped[str]): Unique email address of the user, indexed for fast retrieval.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
