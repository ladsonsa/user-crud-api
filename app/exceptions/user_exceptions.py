class UserNotFoundError(Exception):
    """Raised when a requested user entity cannot be found in the database."""

    pass


class DuplicateUserEmailError(Exception):
    """Raised when an operation attempts to register or update a user with an email that is already in use."""

    pass


class DatabaseOperationError(Exception):
    """Raised when an unrecoverable database or persistence operation fails."""

    pass


class ForeignKeyViolationError(Exception):
    """Raised when a database deletion or update violates a foreign key constraint."""

    pass
