from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponseDTO(BaseModel):
    """Data transfer object for user API responses.

    Attributes:
        id (int): Unique identifier of the user.
        name (str): Full name of the user.
        email (EmailStr): Validated email address of the user.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr