from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.config.dependencies import get_auth_controller
from app.controllers.auth_controller import AuthController
from app.dtos.login import LoginDTO
from app.dtos.token_response import TokenResponseDTO
from app.security.token import create_access_token

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
    """Authenticates user credentials and issues a structured JWT access token DTO.

    Args:
        data (LoginDTO): The validated login credentials request payload.
        controller (AuthController): The authentication controller supplied by dependency injection.

    Returns:
        TokenResponseDTO: A validated DTO containing the generated access token and token type.
    """
    user = controller.authenticate_user(data)
    access_token = create_access_token(str(user.id))

    return TokenResponseDTO(
        access_token=access_token,
        token_type="bearer",
    )
