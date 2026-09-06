from fastapi import HTTPException, status

from app.models.user_model import UserModel


def ensure_user_ownership(
    current_user: UserModel,
    user_id: int,
) -> None:
    """Verifies that the authenticated user matches the requested target user resource ID.

    Args:
        current_user (UserModel): The currently authenticated user instance.
        user_id (int): The target user ID to validate access permissions against.

    Raises:
        HTTPException: HTTP 403 FORBIDDEN if the current user ID does not match the target user ID.
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this user.",
        )
