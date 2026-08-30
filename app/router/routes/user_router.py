from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session

from app.config.dependencies import get_user_controller
from app.database.session import get_db_session
from app.dtos.user_create import UserCreateDTO
from app.dtos.user_response import UserResponseDTO
from app.dtos.user_update import UserUpdateDTO

router = APIRouter(prefix="/api/v1/users", tags=["Users"])
SessionDep = Annotated[Session, Depends(get_db_session)]


@router.post(
    "",
    response_model=UserResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    data: UserCreateDTO,
    session: SessionDep,
) -> UserResponseDTO:
    """Handles the endpoint to register a new user in the system.

    Args:
        data (UserCreateDTO): The payload containing details for creating the user.
        session (Session, optional): The database session supplied by the dependency.

    Returns:
        UserResponseDTO: The created user resource formatted as a response DTO.
    """
    controller = get_user_controller(session)
    return controller.create_user(data)


@router.get(
    "",
    response_model=list[UserResponseDTO],
)
def list_users(
    session: SessionDep,
) -> list[UserResponseDTO]:
    """Handles the endpoint to retrieve all registered users.

    Args:
        session (Session, optional): The database session supplied by the dependency.

    Returns:
        list[UserResponseDTO]: A list containing response DTOs for all stored users.
    """
    controller = get_user_controller(session)
    return controller.list_users()


@router.get(
    "/{user_id}",
    response_model=UserResponseDTO,
)
def get_user(
    user_id: Annotated[int, Path(gt=0, le=2147483647)],
    session: SessionDep,
) -> UserResponseDTO:
    """Handles the endpoint to retrieve a single user by their unique identifier.

    Args:
        user_id (int): The unique identifier of the user to fetch.
        session (SessionDep): The database session supplied by dependency injection.

    Returns:
        UserResponseDTO: The requested user resource formatted as a response DTO.
    """
    controller = get_user_controller(session)
    return controller.get_user(user_id)


@router.put(
    "/{user_id}",
    response_model=UserResponseDTO,
)
def update_user(
    user_id: Annotated[int, Path(gt=0, le=2147483647)],
    data: UserUpdateDTO,
    session: SessionDep,
) -> UserResponseDTO:
    """Handles the endpoint to update an existing user's information.

    Args:
        user_id (int): The unique identifier of the user to update.
        data (UserUpdateDTO): The data transfer object containing updated user attributes.
        session (SessionDep): The database session supplied by dependency injection.

    Returns:
        UserResponseDTO: The updated user resource formatted as a response DTO.
    """
    controller = get_user_controller(session)
    return controller.update_user(user_id, data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: int,
    session: SessionDep,
) -> None:
    """Handles the endpoint to remove a user from the system by their unique identifier.

    Args:
        user_id (int): The unique identifier of the user to delete.
        session (Session, optional): The database session supplied by the dependency.
    """
    controller = get_user_controller(session)
    controller.delete_user(user_id)
