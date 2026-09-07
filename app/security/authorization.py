from app.exceptions.user_exceptions import UserOwnershipError
from app.models.user_model import UserModel


def ensure_user_ownership(current_user: UserModel, user_id: int) -> None:
    """Verifies that the authenticated user matches the requested user resource ID.

    Args:
        current_user (UserModel): The currently authenticated user instance.
        user_id (int): The target user resource identifier to check ownership against.

    Raises:
        UserOwnershipError: If the authenticated user's ID does not match the specified user ID.
    """
    if current_user.id != user_id:
        raise UserOwnershipError
