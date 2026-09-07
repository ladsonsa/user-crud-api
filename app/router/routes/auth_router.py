from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.config.dependencies import get_auth_controller
from app.controllers.auth_controller import AuthController
from app.dtos.login import LoginDTO
from app.dtos.token_response import TokenResponseDTO

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post(
    "/login",
    response_model=TokenResponseDTO,
    status_code=status.HTTP_200_OK,
)
def login(
    data: LoginDTO,
    controller: Annotated[AuthController, Depends(get_auth_controller)],
) -> TokenResponseDTO:
    """Handles the endpoint for user authentication and access token generation.

    Args:
        data (LoginDTO): The payload containing user login credentials.
        controller (AuthController): The authentication controller injected via dependency.

    Returns:
        TokenResponseDTO: Response DTO containing the issued JWT access token and token type.
    """
    return controller.authenticate_user(data)
